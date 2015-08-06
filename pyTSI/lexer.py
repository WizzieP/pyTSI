import ply.lex as lex

tokens = (
    'TSINFO',
    'TREE_NAME',
    'END_TREE',
    'ATTR',
    'ATTR_NAME',
    'NODE_NAME',
    'REF_ATTR_NAME',
    'REF_NODE_NAME',
    'NODE',
    'END_NODE',
    'TREE',
    'AS_NODE',
    'REF_ATTR',
    'REF_NODE',
    'END_REF_NODE',
    'VALUE',
    'NEWLINES',
    'IN_MODE',
    'COMMENT',
    'COMMENT_TEXT',
)

t_TSINFO = r'treestructinfo'
t_TREE_NAME = r'name'
t_END_TREE = r'end\s{1}tree'
t_ATTR = r'attr'
t_NODE = r'node'
t_END_NODE = r'end\s{1}node'
t_TREE = r'tree'
t_AS_NODE = r'as\s{1}node'
t_REF_ATTR = r'ref\s{1}attr'
t_REF_NODE = r'ref\s{1}node'
t_END_REF_NODE = r'end\s{1}ref\s{1}node'
t_IN_MODE = r'in\s{1}mode'
t_COMMENT = r'::'

def t_NEWLINES(t):
    r'\n\s*'
    count = t.value.count('\n')
    t.lexer.lineno += count
    return t

def t_COMMENT_TEXT(t):
    r'(?<=::)(.+?)(?=\n)'
    t.value = t.value.strip()
    return t

def t_ATTR_NAME(t):
    r'(?<=attr)(?<!ref\s{1}attr)(.+?)(?=")'
    t.value = t.value.strip()
    return t

def t_REF_ATTR_NAME(t):
    r'(?<=ref\s{1}attr)(.+?)(?=[\n"])'
    t.value = t.value.strip()
    return t

def t_REF_NODE_NAME(t):
    r'(?<=ref\s{1}node)(.+?)(?=\n)'
    t.value = t.value.strip()
    return t

def t_NODE_NAME(t):
    r'(?<=node)(?<!ref\s{1}node)(.+?)(?=\n)'
    t.value = t.value.strip()
    return t


def t_VALUE(t):
    r'"(.*)"'
    t.value = t.value[1:-1]  # cut the quotes
    return t

t_ignore_WHITESPACE = r'[ \t]'

lexer = lex.lex(debug=True)

def tokenize(input):
    lexer.input(input)
    return tokens_stream_to_list()

def tokens_stream_to_list():
    tokens = []
    for token in lexer:
        tokens.append(token)
    return tokens