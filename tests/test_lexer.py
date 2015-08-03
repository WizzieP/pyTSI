import unittest
import pyTSI.lexer as lexer


class TestLexer(unittest.TestCase):
    def test_empty_tree(self):
        tokens = lexer.tokenize('treestructinfo "2.0"\nend tree')
        self.assertEqual(tokens[0].type, 'TSINFO')
        self.assertEqual(tokens[1].type, 'VALUE')
        self.assertEqual(tokens[1].value, '2.0')
        self.assertEqual(tokens[2].type, 'NEWLINES')
        self.assertEqual(tokens[3].type, 'END_TREE')

    def test_tree_with_some_attrs(self):
        tokens = lexer.tokenize('treestructinfo "2.0"\nattr Some Attr "Some Value"\nattr Some Other Attr ""\nend tree')
        self.assertEqual(tokens[3].type, 'ATTR')
        self.assertEqual(tokens[4].type, 'ATTR_NAME')
        self.assertEqual(tokens[4].value, 'Some Attr')
        self.assertEqual(tokens[5].value, 'Some Value')
        self.assertEqual(tokens[8].value, 'Some Other Attr')
        self.assertEqual(tokens[9].value, '')

    def test_tree_with_ref_node(self):
        tokens = lexer.tokenize('treestructinfo "2.0"\nref node Some Node\nend tree\n'
                                'ref node Some Node\nattr Some Attr "Foo"\nend ref node')

