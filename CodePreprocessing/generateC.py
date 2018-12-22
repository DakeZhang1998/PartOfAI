import json

f = open('sample.json', errors='ignore')
st = f.read()
text = json.loads(st)
tokens = text['tokens']
head_String =''
C_String = ''
entity_counter = 1
line_num = tokens[0]['line']
formals = []
flag = False
variable_match = {}
for token in tokens:
    if token['line']>line_num:
        line_num=token['line']
        C_String+='\n'
    if token['kind']=='Keyword' and token['sem']=='FunctionDecl':
        #C_String+='int '
        continue
    elif token['kind']=='Identifier' and token['sem']=='FunctionDecl':
        #C_String = C_String + token['text'] + " "
        continue
    elif token['kind']=='Punctuation' and token['sem']=='FunctionDecl':
        #C_String = C_String + token['text'] + " "
        continue
    elif token['kind']=='Identifier' and token['sem']=="ParmDecl":
        variable_match[token['text']] = "entity_" + str(entity_counter)
        entity_counter += 1
        variable_name = token['sym']['type']+variable_match[token['text']]
        formals.append(variable_name)
    elif token['sem']=="ParmDecl":
        continue
    elif token['kind'] == 'Identifier' and tokens[tokens.index(token)-1]['text']=='='\
        and tokens[tokens.index(token)-1]['kind']=='Identifier' and token['sem']=='DeclRefExpr':
        if 'sym' in token and token['sym']!=None:
            C_String = C_String + "rand();"
            over_look = True
    elif token['kind'] == 'Identifier':
        if token['text'] in variable_match:
            C_String = C_String + variable_match[token['text']] + " "
        else:
            variable_match[token['text']]="entity_"+str(entity_counter)
            entity_counter+=1
            C_String = C_String + variable_match[token['text']] + " "
    else:
        C_String = C_String + token['text'] + " "
for formal in formals:
    formal_string = ''
    if '[' in formal and ']' in formal:
        if 'char' in formal:
            formal_string = 'char '+ formal[formal.index(']')+1:]+'[10];'
        elif 'int' in formal:
            formal_string = 'int ' + formal[formal.index(']') + 1:] + '[10];'
    elif '*' in formal:
        if 'char' in formal:
            formal_string = 'char '+ formal[formal.index('entity'):]+'[10];'
        elif 'int' in formal:
            formal_string = 'int ' + formal[formal.index('entity'):] + '[10];'
    else:
        if 'char' in formal:
            formal_string = 'char '+ formal[formal.index('entity'):]+'=\'a\';'
        elif 'int' in formal:
            formal_string = 'int ' + formal[formal.index('entity'):] + '=10;'
    head_String = head_String + formal_string+'\n'
print(head_String)
print(C_String)