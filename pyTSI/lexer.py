import ply.lex as lex
    
    
class Lexer:
        
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

    def __init__(self):
        self.lexer = lex.lex(module=self)
    
    def t_NEWLINES(self, t):
        r'\n\s*'
        count = t.value.count('\n')
        t.lexer.lineno += count
        return t
    
    def t_COMMENT_TEXT(self, t):
        r'(?<=::)(.+?)(?=\n)'
        t.value = t.value.strip()
        return t
    
    def t_ATTR_NAME(self, t):
        r'(?<=attr)(?<!ref\s{1}attr)(.+?)(?=")'
        t.value = t.value.strip()
        return t
    
    def t_REF_ATTR_NAME(self, t):
        r'(?<=ref\s{1}attr)(.+?)(?=[\n"])'
        t.value = t.value.strip()
        return t
    
    def t_REF_NODE_NAME(self, t):
        r'(?<=ref\s{1}node)(.+?)(?=\n)'
        t.value = t.value.strip()
        return t
    
    def t_NODE_NAME(self, t):
        r'(?<=node)(?<!ref\s{1}node)(?<!as\s{1}node)(.+?)(?=\n)'
        t.value = t.value.strip()
        return t
    
    
    def t_VALUE(self, t):
        r'"(.*?)"'
        t.value = t.value[1:-1]  # cut the quotes
        return t
    
    t_ignore_WHITESPACE = r'[ \t]'

    
    def tokenize(self, input):
        self.lexer.input(input)
        return self._tokens_stream_to_list()
    
    def _tokens_stream_to_list(self):
        tokens = []
        for token in self.lexer:
            tokens.append(token)
        return tokens
