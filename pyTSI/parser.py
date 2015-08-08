import ply.yacc as yacc
from .lexer import Lexer
from .elements import Attr, Node
from collections import deque


class Parser:

    def __init__(self):

        # global deque with declarations of referenced elements
        # if state == 'tree', append to the left (FIFO), otherwise append to the right (LIFO)
        # pop the same way
        self.refs = deque()

        # referenced elements are parsed in recursive order, so we need a list to put them in deque in correctly
        # elements in `local_refs` are put to the left of `refs` after end of each ref node declaration
        self.local_refs = []

        self.tokens = Lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, input):
        lexer = Lexer().lexer
        return self.parser.parse(input + '\n', lexer)


    def p_tree(self, p):
        '''tree : treeheader elementList END_TREE
                | treeheader elementList END_TREE seen_END_TREE refsElementList'''
        p[0] = Node('', p[2])

    def p_treeheader(self, p):
        '''treeheader : TSINFO VALUE
                      | TSINFO VALUE TREE_NAME VALUE'''
        if p[2] != '2.0':
            raise SyntaxError

    def p_elementList_empty(self, p):
        'elementList : NEWLINES'
        p[0] = []

    def p_elementList_nonempty(self, p):
        'elementList : elementList element'
        p[0] = p[1]
        p[0].append(p[2])

    def p_element(self, p):
        '''element : attr
                   | node
                   | refAttrDeclaration
                   | refNodeDeclaration
                   | linkedTree'''
        p[0] = p[1]

    def p_attr(self, p):
        'attr : ATTR ATTR_NAME valueList'
        p[0] = Attr(p[2], p[3])

    def p_valueList_single(self, p):
        'valueList : VALUE NEWLINES'
        p[0] = p[1]

    def p_valueList_multiple(self, p):
        'valueList : valueList VALUE NEWLINES'
        p[0] = p[1]
        p[0] = p[0] + '\n' + p[2]

    def p_node(self, p):
        'node : NODE NODE_NAME elementList END_NODE NEWLINES'
        p[0] = Node(p[2], p[3])

    def p_refAttrDeclaration(self, p):
        'refAttrDeclaration : REF_ATTR REF_ATTR_NAME NEWLINES'
        attr = Attr(p[2], None)
        p[0] = attr
        self.local_refs.append(attr)

    def p_refNodeDeclaration(self, p):
        'refNodeDeclaration : REF_NODE REF_NODE_NAME NEWLINES'
        node = Node(p[2], None)
        p[0] = node
        self.local_refs.append(node)

    def p_seen_END_TREE(self, p):
        'seen_END_TREE : '
        self.refs.extend(self.local_refs)
        self.local_refs = []

    def p_refsElementList_empty(self, p):
        'refsElementList : NEWLINES'

    def p_refsElementList_nonempty(self, p):
        'refsElementList : refsElementList refElement'

    def p_refElement(self, p):
        '''refElement : refAttrDefinition
                      | refNodeDefinition
        '''
        p[0] = p[1]

    def p_refAttrDefinition(self, p):
        'refAttrDefinition : REF_ATTR REF_ATTR_NAME valueList'
        attr = self.refs.popleft()
        attr.value = p[3]
        self.refs.extendleft(self.local_refs)

    def p_refNodeDefinition(self, p):
        'refNodeDefinition : REF_NODE REF_NODE_NAME elementList END_REF_NODE NEWLINES'
        node = self.refs.popleft()
        node.elements = p[3]
        self.refs.extendleft(reversed(self.local_refs))
        self.local_refs = []

    def p_linkedTree_simple(self, p):
        'linkedTree : TREE VALUE AS_NODE VALUE NEWLINES'
        tree = get_linked_tree(p[2])
        tree.name = p[4]
        p[0] = tree

    def p_linkedTree_extended(self, p):
        'linkedTree : TREE VALUE AS_NODE VALUE IN_MODE valueList'
        flags = p[6].split('\n')
        file_flag = 'r'
        if 'text' and 'binary' in flags:
            raise SyntaxError('File cannot be in text and binary at the same moment')
        if 'binary' in flags:
            file_flag += 'b'
        if 'write' in flags:
            file_flag += '+'

        tree = get_linked_tree(p[2], file_flag)
        tree.name = p[4]
        p[0] = tree


def get_linked_tree(file_name, mode='r'):
    with open(file_name, mode) as file:
        tree = Parser().parse(file.read())
        tree.link_file_name = file_name
        return tree
