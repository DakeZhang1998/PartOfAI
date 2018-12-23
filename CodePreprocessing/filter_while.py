import json
import uuid


# 全局变量区
variable_match = {}                    # 字典，键是变量原名，值为变量的新名(e.g. var_1)
entity_counter = 1                     # 计数，用来替换变量名


# 传入解码后的json文件，返回一个字符串数组，其中的每一个元素都是一个function
def get_functions(file_content):
    functions = []                                      # 存储返回的字符串数组
    tokens = file_content['tokens']                     # 存储所有读取的token
    str_function_head = '#include <stdlib.h>\n#include <string.h>\n'          # 保存 #include<stdlib.h> 和 struct 信息

    # 当读到'FunctionDecl'类型的token时，开始加入元素，同时记录'{'和'}'的匹配情况，
    # 如果完全匹配，则调用get_function函数得到一个字符串结果
    index = 0
    while index < len(tokens):
        # 保存所有的struct
        index2 = index
        current_token = tokens[index2]
        if current_token['sem'] == 'StructDecl' and current_token['text'] == 'struct':
            line_num_temp = current_token['line']
            left_brace_num = 0
            right_brace_num = 0
            while index2 < len(tokens):
                current_token = tokens[index2]
                if current_token['kind'] == 'Identifier':
                    str_function_head += variable_id(current_token['text']) + ' '
                else:
                    str_function_head += current_token['text'] + ' '
                if line_num_temp < current_token['line']:
                    str_function_head += '\n'
                if current_token['text'] == '{':
                    left_brace_num += 1
                elif current_token['text'] == '}':
                    right_brace_num += 1
                    if left_brace_num == right_brace_num and left_brace_num != 0:
                        str_function_head += ';\n'
                        break
                index2 += 1
            index = index2 + 1
            continue

        if current_token['sem'] == 'StructDecl' and current_token['kind'] == 'Identifier':
            str_function_head += 'typedef struct '
            line_num_temp = current_token['line']
            left_brace_num = 0
            right_brace_num = 0
            while index2 < len(tokens):
                current_token = tokens[index2]
                if current_token['kind'] == 'Identifier':
                    str_function_head += variable_id(current_token['text']) + ' '
                else:
                    str_function_head += current_token['text'] + ' '
                if line_num_temp < current_token['line']:
                    str_function_head += '\n'
                if current_token['text'] == '{':
                    left_brace_num += 1
                elif current_token['text'] == '}':
                    right_brace_num += 1
                    if left_brace_num == right_brace_num and left_brace_num != 0:
                        break
                index2 += 1
            index = index2 + 1
            current_token = tokens[index]
            if current_token['kind'] == 'Identifier':
                str_function_head += variable_id(current_token['text']) + ';\n'
            continue

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
                    if left_brace_num == right_brace_num and left_brace_num != 0:
                        break
                temp_tokens.append(current_token)
                index2 += 1

            # 将得到的分割好的token序列
            temp_str = 'int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; } \n' \
                       'int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; } \n' \
                       'void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t); \n' \
                       'void pthread_cond_signal(struct pthread_cond_t* cond_t);\n'
            functions.append(str_function_head + temp_str + get_function(temp_tokens))
            index = index2 + 1
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
    index = 0                       # 扫描时，当前的位置
    reserved_functions = ['pthread_cond_wait', 'pthread_cond_signal',
                          'pthread_mutex_lock', 'pthread_mutex_unlock',
                          'strcpy', 'strncpy', 'free']

    # 开始扫描tokens
    while index < len(tokens):
        current_token = tokens[index]                   # 当前读到的token

        # 用于测试时快速定位到某一行，正常使用可以注释掉
        if current_token['line'] == 19:
            print('I am here!')

        if tokens[index]['text'] == 'else' and tokens[index+1]['text'] == 'if':
            print('hello!')

        # 进行换行
        if current_token['line'] > line_num:
            line_num = tokens[index]['line']
            body_str += '\n'

        # 先处理函数头，即'void foo(int i, int arr[])'
        if current_token['kind'] == 'Keyword' and current_token['sem'] == 'FunctionDecl':
            index2 = index + 1
            head_str += 'int main() {\n'
            # 一口气读到'('
            while index2 < len(tokens):
                if tokens[index2]['text'] == '(':
                    break
                index2 += 1
            # 在一口气读到')'
            params = []
            index2 += 1
            while index2 < len(tokens):
                current_token = tokens[index2]
                if current_token['text'] == ')':
                    break
                params.append(current_token)
                index2 += 1
            index = index2 + 2
            head_str += params_exe(params)
            continue

        # 保留reserved_functions中的函数调用，一直读到最后一个';'，执行完之后直接跳到下一次循环
        if current_token['text'] in reserved_functions and current_token['kind'] == 'Identifier':
            index2 = index
            while index2 < len(tokens):
                current_token = tokens[index2]
                # 参数变量名转换
                if current_token['kind'] == 'Identifier' and index2 > index:
                    body_str += variable_id(current_token['text']) + ' '
                else:
                    body_str += current_token['text'] + ' '
                index2 += 1
                # 满足情况跳出循环
                if current_token['text'] == ';':
                    break
            index = index2
            continue

        # 类似于'pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);'单纯的函数调用，直接干掉
        # 由于上一步已经保留了需要保留的函数调用，所以不需要再进行判断
        # 如果是赋值运算，例如'i = foo();'，则替换为rand()，同理'if(foo())'的情况
        # 判断前一个token是否为'}'或者';'
        not_functions = ['malloc']
        if current_token['kind'] == 'Identifier' and tokens[index + 1]['text'] == '(' and index > 1\
                and current_token['text'] not in not_functions:
            if tokens[index - 1]['text'] == '}' or tokens[index - 1]['text'] == ';' or tokens[index - 1]['text'] == '{'\
                    or tokens[index - 1]['text'] == ')':
                index2 = index
                # 直接去掉
                while index2 < len(tokens):
                    current_token = tokens[index2]
                    if current_token['text'] == ';':
                        break
                    index2 += 1
                index = index2 + 1
                continue
            else:
                # 换成rand()
                index2 = index
                left_bracket_num = 0
                right_bracket_num = 0
                while index2 < len(tokens):
                    current_token = tokens[index2]
                    # 读到左右括号匹配即可跳出循环
                    if current_token['text'] == '(':
                        left_bracket_num += 1
                    elif current_token['text'] == ')':
                        right_bracket_num += 1
                    if left_bracket_num == right_bracket_num and left_bracket_num != 0:
                        break
                    index2 += 1
                if tokens[index2]['text'] == ';':
                    body_str += '; '
                index = index2 + 1
                body_str += 'rand() '
                continue

        # 遇到return语句，直接删除
        if current_token['text'] == 'return':
            index2 = index
            while index2 < len(tokens):
                current_token = tokens[index2]
                index2 += 1
                if current_token['text'] == ';':
                    break
            index = index2
            continue

        # 不接受double/float/short/void类型，全部改成int，注意，此处未处理long double，接受unsigned int
        except_keywords = ['double', 'float', 'short', 'void']
        if current_token['kind'] == 'Keyword' and current_token['text'] in except_keywords:
            body_str += 'int '
            index += 1
            continue

        # 如果当前是token的kind是'Identifier'，则调用函数，返回'var_i'，放在最后处理
        if current_token['kind'] == 'Identifier' and current_token['text']:
            # 如果是NULL的话，直接添加
            if current_token['text'] == 'NULL':
                body_str += 'NULL '
            elif current_token['text'] in not_functions:
                body_str += current_token['text']
            else:
                body_str += variable_id(current_token['text']) + ' '
            index += 1
            continue

        # 不属于以上任意一种情况，则正常添加
        body_str += current_token['text'] + ' '
        index += 1

    return head_str + body_str


# 用于处理所有的变量名，参数为当前的token的'text'属性，返回变量的新名，格式为'var_1'
def variable_id(token_text):
    global variable_match         # 全局变量，字典，键是变量原名，值为变量的新名(e.g. var_1)
    global entity_counter         # 全局变量，计数，用来替换变量名

    # 判断当前变量名是否已经存档，如果已存档过，则返回对应的变量名，反之则指定新的变量名
    if token_text not in variable_match.keys():
        variable_match[token_text] = "var_" + str(entity_counter)
        entity_counter += 1

    return variable_match[token_text]


# 用于处理函数声明中的形参，由于形参的值未知，所以值都赋为rand()，输入为参数列表，输出为对应的变量声明和赋值
def params_exe(params):
    result = ''
    index = 0

    while index < len(params):
        current_token = params[index]
        if current_token['text'] == ',':
            index += 1
            continue

        # 开始正常处理函数
        if current_token['kind'] == 'Keyword':
            # 处理的类型，'int i'/'int * i'/'int i[]'
            if current_token['text'] == 'int' or current_token['text'] == 'char':
                result += current_token['text'] + ' '
                index += 1
                current_token = params[index]
                # 处理'int *i'
                if current_token['text'] == '*':
                    index += 1
                    current_token = params[index]
                    if current_token['kind'] == 'Identifier':
                        result += variable_id(current_token['text']) + ' [10] ;\n'
                        index += 1
                        continue
                # 处理'ind i'/'int i[]'
                elif current_token['kind'] == 'Identifier':
                    result += variable_id(current_token['text']) + ' '
                    index += 1
                    if index < len(params):
                        current_token = params[index]
                        if current_token['text'] == '[':
                            index += 1
                            current_token = params[index]
                            if current_token['text'] == ']':
                                index += 1
                                result += '[ 10 ] ;\n'
                                continue
                            elif current_token['sem'] == 'IntegerLiteral':
                                result += ' [' + current_token['text'] + ' ] ;\n'
                                index += 2
                                continue
                        result += '= rand() ;\n'
                    else:
                        result += '= rand() ;\n'
                        continue
            else:
                result += 'int '
                index += 1
                current_token = params[index]
                # 处理'double *i'
                if current_token['text'] == '*':
                    index += 1
                    current_token = params[index]
                    if current_token['kind'] == 'Identifier':
                        result += variable_id(current_token['text']) + ' [10] ;\n'
                        index += 1
                        continue
                # 处理'double i'/'double i[]'
                elif current_token['kind'] == 'Identifier':
                    result += variable_id(current_token['text']) + ' '
                    index += 1
                    current_token = params[index]
                    if current_token['text'] == '[':
                        index += 1
                        current_token = params[index]
                        if current_token['text'] == ']':
                            index += 1
                            result += '[ rand() ] ;\n'
                            continue
                        elif current_token['sem'] == 'IntegerLiteral':
                            result += ' [' + current_token['text'] + ' ] ;\n'
                            index += 2
                            continue
                        result += '= rand() ;\n'
                    else:
                        result += '= rand() ;\n'
                        continue
        index += 1
    return result


if __name__ == '__main__':
    file_name = 'malloc-2'
    file = open('changeCode/' + file_name + '.json', errors='ignore')
    file_content = json.loads(file.read())

    result = get_functions(file_content)
    # for function in result:
    function = result[len(result) - 1]
    function = function[0:len(function)-1]
    function += 'return 0; \n }'
    f = open('changeCode/' + file_name + '_' + str(uuid.uuid1()) + '.c', errors='ignore', mode='w')
    # f = open(str(uuid.uuid1())+'.c', errors='ignore', mode='w')
    f.write(function)
    # print(function)
    # print('-----------------------------')

