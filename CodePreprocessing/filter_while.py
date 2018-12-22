import json
import uuid


# 全局变量区
variable_match = {}                    # 字典，键是变量原名，值为变量的新名(e.g. var_1)
entity_counter = 1                     # 计数，用来替换变量名


# 传入解码后的json文件，返回一个字符串数组，其中的每一个元素都是一个function
def get_functions(file_content):
    functions = []                           # 存储返回的字符串数组
    tokens = file_content['tokens']          # 存储所有读取的token

    # 当读到'FunctionDecl'类型的token时，开始加入元素，同时记录'{'和'}'的匹配情况，
    # 如果完全匹配，则调用get_function函数得到一个字符串结果
    index = 0
    while index < len(tokens):
        # 当读到'FunctionDecl'类型的token时，开始加入元素
        if tokens[index]['sem'] == 'FunctionDecl':
            temp_tokens = []

            # 去除简单的函数声明
            # 如果是形如'int func(int, int);'的函数声明，需要去掉，这里假设符号的sem属性为'FunctionDecl'
            # 先一口气扫描到')'，然后判断下一个字符是不是'{'，如果是，则进行函数分割；反之，说明是形如上面提到的函数声明，干掉
            index2 = index
            while index2 < len(tokens):
                current_token = tokens[index2]
                if current_token['text'] == ')' and current_token['sem'] == 'FunctionDecl':
                    break
                index2 += 1
            # 如果下一个是'{'的话，就不做处理；否则，就跳过
            if index2 < len(tokens) - 1 and tokens[index2 + 1]['text'] != '{':
                index = index2 + 1
                continue

            # 进行正常的函数分割
            left_brace_num = 0
            right_brace_num = 0
            index2 = index
            while index2 < len(tokens):
                current_token = tokens[index2]
                if current_token['text'] == '{':
                    left_brace_num += 1
                elif current_token['text'] == '}':
                    right_brace_num += 1
                    if left_brace_num == right_brace_num:
                        break
                temp_tokens.append(current_token)
                index2 += 1

            # 将得到的分割好的token序列
            functions.append(get_function(temp_tokens))
            index = index2 + 1
            print(temp_tokens)
        else:
            index += 1

    return functions


# 传入上一步切割好的token数组，返回一个字符串，为一个function
def get_function(tokens):
    global entity_counter  # 全局变量，字典，键是变量原名，值为变量的新名(e.g. var_1)
    global variable_match  # 全局变量，计数，用来替换变量名

    result_function = ''            # 最后返回的处理好的一个函数
    head_str = ''                   # 用于存放函数声明中的参数，由于不知道准确值，因而用rand()赋值
    body_str = ''                   # 用于存放转化后的函数体

    line_num = tokens[0]['line']    # 记录当前的行号，用来进行换行操作
    formals = []
    variable_match = {}             # 全局变量，
    index = 0                       # 扫描时，当前的位置
    entity_counter = 1  # 全局变量，
    reserved_functions = ['pthread_cond_wait', 'pthread_cond_signal',
                          'pthread_mutex_lock', 'pthread_mutex_unlock']

    # 开始扫描tokens
    while index < len(tokens):
        current_token = tokens[index]                   # 当前读到的token

        # 用于测试时快速定位到某一行，正常使用可以注释掉
        if current_token['line'] == 19:
            print('I am here!')

        if tokens[index]['text'] == 'else' and tokens[index+1]['text'] == 'if':
            print('hello!')

        # 进行换行
        if tokens[index]['line'] > line_num:
            line_num = tokens[index]['line']
            body_str += '\n'

        # 保留reserved_functions中的函数调用，一直读到最后一个';'，执行完之后直接跳到下一次循环
        if current_token['text'] in reserved_functions and current_token['kind'] == 'Identifier':
            index2 = index
            while index2 < len(tokens):
                current_token = tokens[index2]
                # 参数变量名转换
                if current_token['kind'] == 'Identifier' and index2 > index:
                    body_str += viarable_id(current_token['text']) + ' '
                else:
                    body_str = body_str + current_token['text'] + ' '
                index2 += 1
                # 满足情况跳出循环
                if current_token['text'] == ';':
                    break
            index = index2 + 1
            continue

        # 类似于'pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);'单纯的函数调用，直接干掉
        # 由于上一步已经保留了


        # 收集函数参数，将其作为函数开始后的变量声明
        if tokens[index]['kind'] == 'Identifier' and tokens[index]['sem'] == "ParmDecl":
            variable_match[tokens[index]['text']] = "entity_" + str(entity_counter)
            entity_counter += 1
            variable_name = tokens[index]['sym']['type'] + variable_match[tokens[index]['text']]
            formals.append(variable_name)      # formals 后面再处理
        elif tokens[index]['sem'] == "ParmDecl":
            index+=1                               # 函数参数中其他部分直接忽略

        # 形如 int index = foo()形式的，直接将foo()替换为rand()
        elif tokens[index]['kind'] == 'Identifier' and tokens[index-1]['text'] == '=' \
                and tokens[index-2]['kind'] == 'Identifier' and tokens[index]['sem'] == 'DeclRefExpr':
            if 'sym' in tokens[index] and tokens[index]['sym'] != None:
                body_str = body_str + "rand();"
                index+=1
                while tokens[index]['text']!=';':    # 遇到;作为结束标志
                    index+=1
        # 处理形如while(foo()) while(!foo()) if(foo()) if(!foo())形式
        elif tokens[index]['kind'] == 'Identifier' and (tokens[index-1]['text'] == '('or tokens[index-1]['text'] == '!') \
                and (tokens[index-1]['sem'] == 'IfStmt' or tokens[index-1]['sem'] == 'WhileStmt'or tokens[index-1]['sem']=='DeclRefExpr' or tokens[index-1]['sem']=='UnaryOperator'):
                body_str = body_str + "rand()"
                counter = 1
                while counter != 0:       # 防止多个括号的出现 如 foo(foo()) 取最后一个括号
                    index+=1
                    if tokens[index]['text']=='(':
                        counter+=1
                    elif tokens[index]['text']==')':
                        counter-=1
                body_str = body_str + ")"
        # 对于这样foo()独占一行的函数，直接去掉
        elif tokens[index]['kind'] == 'Identifier' and tokens[index]['sem']=='DeclRefExpr' and tokens[index]['line']>tokens[index-1]['line'] :
            if 'sym' in tokens[index] and tokens[index]['sym']!=None and tokens[index]['sym']['kind']=='FunctionDecl':
                if tokens[index-1]['text'] != '(' and tokens[index-1]['text'] != '=':
                    index += 1
                    while tokens[index]['text'] != ';':
                        index += 1
            else:
                if tokens[index]['text'] in variable_match:
                    body_str = body_str + variable_match[tokens[index]['text']] + " "
                else:
                    variable_match[tokens[index]['text']] = "entity_" + str(entity_counter)
                    entity_counter += 1
                    body_str = body_str + variable_match[tokens[index]['text']] + " "
        # 变量命名映射
        elif tokens[index]['kind'] == 'Identifier':
            if tokens[index]['text'] in variable_match:
                body_str = body_str + variable_match[tokens[index]['text']] + " "
            else:
                variable_match[tokens[index]['text']] = "entity_" + str(entity_counter)
                entity_counter += 1
                body_str = body_str + variable_match[tokens[index]['text']] + " "
        # 其他的正常打印输出
        else:
            body_str = body_str + tokens[index]['text'] + " "
        index += 1

    for formal in formals:
        formal_string = ''
        # char[] 和 int[]
        if '[' in formal and ']' in formal:
            if 'char' in formal:
                formal_string = 'char ' + formal[formal.index(']') + 1:] + '[10];'
            elif 'int' in formal:
                formal_string = 'int ' + formal[formal.index(']') + 1:] + '[10];'
        elif '*' in formal:
            if 'char' in formal:
                formal_string = 'char ' + formal[formal.index('entity'):] + '[10];'
            elif 'int' in formal:
                formal_string = 'int ' + formal[formal.index('entity'):] + '[10];'
        # char 与 int类型
        else:
            if 'char' in formal:
                formal_string = 'char ' + formal[formal.index('entity'):] + '=\'a\';'
            elif 'int' in formal:
                formal_string = 'int ' + formal[formal.index('entity'):] + '=rand();'
        head_str = head_str + formal_string + '\n'

    return head_str + body_str


# 用于处理所有的变量名，参数为当前的token的'text'属性，返回变量的新名，格式为'var_1'
def viarable_id(token_text):
    global variable_match         # 全局变量，字典，键是变量原名，值为变量的新名(e.g. var_1)
    global entity_counter         # 全局变量，计数，用来替换变量名

    # 判断当前变量名是否已经存档，如果已存档过，则返回对应的变量名，反之则指定新的变量名
    if token_text not in variable_match.keys():
        variable_match[token_text] = "var_" + str(entity_counter)
        entity_counter += 1

    return variable_match[token_text]


if __name__ == '__main__':
    file = open('test/while.json', errors='ignore')
    file_content = json.loads(file.read())

    result = get_functions(file_content)
    for function in result:
        function = "int main(){\n"+function
        function = function + "\n}"
        f = open(str(uuid.uuid1())+'.c', errors='ignore', mode='w')
        f.write(function)
        # print(function)
        # print('-----------------------------')

