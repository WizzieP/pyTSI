import logging
import ply.yacc as yacc
from .lexer import tokens
from .elements import Attr, Node
from collections import namedtuple, deque

# global deque with declarations of referenced elements
# if state == 'tree', append to the left (FIFO), otherwise append to the right (LIFO)
# pop the same way
refs = deque()

# referenced elements are parsed in recursive order, so we need a list to put them in deque in correctly
# elements in `local_refs` are put to the left of `refs` after end of each ref node declaration
local_refs = []

def p_tree(p):
    '''tree : treeheader elementList END_TREE
            | treeheader elementList END_TREE seen_END_TREE refsElementList'''
    p[0] = Node('', p[2])

def p_treeheader(p):
    '''treeheader : TSINFO VALUE
                  | TSINFO VALUE TREE_NAME VALUE'''
    if p[2] != '2.0':
        raise SyntaxError

def p_elementList_empty(p):
    'elementList : NEWLINES'
    p[0] = []

def p_elementList_nonempty(p):
    'elementList : elementList element'
    p[0] = p[1]
    p[0].append(p[2])

def p_element(p):
    '''element : attr
               | node
               | refAttrDeclaration
               | refNodeDeclaration
               | linkedTree'''
    p[0] = p[1]

def p_attr(p):
    'attr : ATTR ATTR_NAME valueList'
    p[0] = Attr(p[2], p[3])

def p_valueList_single(p):
    'valueList : VALUE NEWLINES'
    p[0] = p[1]

def p_valueList_multiple(p):
    'valueList : valueList VALUE NEWLINES'
    p[0] = p[1]
    p[0] = p[0] + '\n' + p[2]

def p_node(p):
    'node : NODE NODE_NAME elementList END_NODE NEWLINES'
    p[0] = Node(p[2], p[3])

def p_refAttrDeclaration(p):
    'refAttrDeclaration : REF_ATTR REF_ATTR_NAME NEWLINES'
    attr = Attr(p[2], None)
    p[0] = attr
    local_refs.append(attr)

def p_refNodeDeclaration(p):
    'refNodeDeclaration : REF_NODE REF_NODE_NAME NEWLINES'
    node = Node(p[2], None)
    p[0] = node
    local_refs.append(node)

def p_seen_END_TREE(p):
    'seen_END_TREE : '
    global local_refs
    refs.extend(local_refs)
    local_refs = []

def p_refsElementList_empty(p):
    'refsElementList : NEWLINES'

def p_refsElementList_nonempty(p):
    'refsElementList : refsElementList refElement'

def p_refElement(p):
    '''refElement : refAttrDefinition
                  | refNodeDefinition
    '''
    p[0] = p[1]

def p_refAttrDefinition(p):
    'refAttrDefinition : REF_ATTR REF_ATTR_NAME valueList'
    attr = refs.popleft()
    attr.value = p[3]
    refs.extendleft(local_refs)

def p_refNodeDefinition(p):
    'refNodeDefinition : REF_NODE REF_NODE_NAME elementList END_REF_NODE NEWLINES'
    node = refs.popleft()
    node._elements = p[3]
    global local_refs
    refs.extendleft(reversed(local_refs))
    local_refs = []

def p_linkedTree_simple(p):
    'linkedTree : TREE VALUE AS_NODE VALUE'
    tree = get_linked_tree(p[2])
    tree.name = p[4]
    p[0] = tree

def p_linkedTree_extended(p):
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
        tree = parse(file.read())
        tree.link_file_name = file_name
        return tree

parser = yacc.yacc()

def clear_variables():
    global local_refs, refs
    refs = deque()
    local_refs = []

def parse(input, debug=False):
    clear_variables()
    return parser.parse(input + '\n')