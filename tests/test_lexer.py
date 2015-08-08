import unittest
from pyTSI.lexer import Lexer


class TestLexer(unittest.TestCase):
    def test_empty_tree(self):
        tokens = Lexer().tokenize('treestructinfo "2.0"\nend tree')
        self.assertEqual(tokens[0].type, 'TSINFO')
        self.assertEqual(tokens[1].type, 'VALUE')
        self.assertEqual(tokens[1].value, '2.0')
        self.assertEqual(tokens[2].type, 'NEWLINES')
        self.assertEqual(tokens[3].type, 'END_TREE')

    def test_tree_with_some_attrs(self):
        tokens = Lexer().tokenize('treestructinfo "2.0"\nattr Some Attr "Some Value"\nattr Some Other Attr ""\nend tree')
        self.assertEqual(tokens[3].type, 'ATTR')
        self.assertEqual(tokens[4].type, 'ATTR_NAME')
        self.assertEqual(tokens[4].value, 'Some Attr')
        self.assertEqual(tokens[5].value, 'Some Value')
        self.assertEqual(tokens[8].value, 'Some Other Attr')
        self.assertEqual(tokens[9].value, '')

    def test_tree_with_ref_node(self):
        tokens = Lexer().tokenize('treestructinfo "2.0"\nref node Some Node\nend tree\n'
                                'ref node Some Node\nattr Some Attr "Foo"\nend ref node')
        self.assertEqual(tokens[3].type, 'REF_NODE')
        self.assertEqual(tokens[4].type, 'REF_NODE_NAME')
        self.assertEqual(tokens[4].value, 'Some Node')
        self.assertEqual(tokens[5].type, 'NEWLINES')
        self.assertEqual(tokens[8].type, 'REF_NODE')
        self.assertEqual(tokens[9].type, 'REF_NODE_NAME')
        self.assertEqual(tokens[9].value, 'Some Node')
        self.assertEqual(tokens[10].type, 'NEWLINES')
        self.assertEqual(tokens[15].type, 'END_REF_NODE')

    def test_empty_tree_with_comment(self):
        tokens = Lexer().tokenize(''':: Main tree
                                   :: comment
                                   treestructinfo "2.0"
                                   end tree''')
        self.assertEqual(tokens[0].type, 'COMMENT')
        self.assertEqual(tokens[1].type, 'COMMENT_TEXT')
        self.assertEqual(tokens[1].value, 'Main tree')
        self.assertEqual(tokens[2].type, 'NEWLINES')
        self.assertEqual(tokens[3].type, 'COMMENT')
        self.assertEqual(tokens[4].type, 'COMMENT_TEXT')
        self.assertEqual(tokens[4].value, 'comment')
        self.assertEqual(tokens[5].type, 'NEWLINES')

    def test_simple_tree_with_comments(self):
        tokens = Lexer().tokenize('''treestructinfo "2.0"
                                     :: Multiline
                                     :: attr comment
                                     attr Foo "Bar"
                                     node Bar
                                       :: Comment
                                       :: inside of node
                                       attr FooBar "FooBar"
                                     end node
                                   end tree''')
        self.assertEqual(tokens[3].type, 'COMMENT')
        self.assertEqual(tokens[4].type, 'COMMENT_TEXT')
        self.assertEqual(tokens[4].value, 'Multiline')
        self.assertEqual(tokens[7].value, 'attr comment')
        self.assertEqual(tokens[17].value, 'Comment')
        self.assertEqual(tokens[20].value, 'inside of node')

    def test_with_linked_tree(self):
        tokens = Lexer().tokenize('''treestructinfo "2.0"
                                     tree "foo.tsinfo" as node "Bar"
                                   end tree''')
        self.assertEqual(tokens[3].type, 'TREE')
        self.assertEqual(tokens[4].value, 'foo.tsinfo')
        self.assertEqual(tokens[5].type, 'AS_NODE')
        self.assertEqual(tokens[6].type, 'VALUE')
        self.assertEqual(tokens[6].value, 'Bar')
        self.assertEqual(tokens[7].type, 'NEWLINES')

