import unittest
from pyTSI.parser import Parser


class ParserTest(unittest.TestCase):
    def test_with_one_attr(self):
        tree = Parser().parse('treestructinfo "2.0"\nattr Foo "Bar"\nend tree')
        self.assertEqual(tree.elements[0].name, 'Foo')
        self.assertEqual(tree.elements[0].value, 'Bar')

    def test_with_one_ref_attr(self):
        tree = Parser().parse(
            'treestructinfo "2.0"\nref attr Some Ref Attr\nend tree\nref attr Some Ref Attr "Some Value"')
        self.assertEqual(tree.elements[0].value, 'Some Value')

    def test_with_multiple_ref_attrs(self):
        tree = Parser().parse('treestructinfo "2.0"\nref attr Some Ref Attr\nref attr Second \n'
                            'ref attr Third\nend tree\nref attr Some Ref Attr "Some Value"\n'
                            'ref attr Second "Second Value"\nref attr Third "Third Value"')
        self.assertEqual(tree.elements[0].value, 'Some Value')
        self.assertEqual(tree.elements[1].value, 'Second Value')
        self.assertEqual(tree.elements[2].value, 'Third Value')

    def test_with_one_ref_node(self):
        tree = Parser().parse('treestructinfo "2.0"\nref node Some Node\nend tree\n'
                            'ref node Some Node\nattr Some Attr "Foo"\nend ref node')
        self.assertEqual(tree.elements[0].name, 'Some Node')
        self.assertEqual(tree.elements[0].elements[0].name, 'Some Attr')
        self.assertEqual(tree.elements[0].elements[0].value, 'Foo')

    def test_with_nested_ref_node(self):
        tree = Parser().parse(''' treestructinfo "2.0"
                                  ref node First
                                end tree
                                ref node First
                                  ref node First Nested
                                end ref node
                                ref node First Nested
                                  attr Foo "Bar"
                                end ref node''')
        self.assertEqual(tree.elements[0].elements[0].elements[0].value, "Bar")  # attr `Foo` in `First Nested` node

    def test_with_many_nested_refs(self):
        tree = Parser().parse(''' treestructinfo "2.0"
                                  ref node First
                                  ref node Second
                                  ref node Third
                                end tree
                                ref node First
                                  ref node First Nested
                                end ref node
                                ref node First Nested
                                  attr Foo "Bar"
                                end ref node
                                ref node Second
                                  ref attr First Attr
                                  ref attr Second Attr
                                end ref node
                                ref attr First Attr "Foo"
                                ref attr Second Attr "Foo2"
                                ref node Third
                                  attr Bar "Foo3"
                                end ref node''')
        self.assertEqual(tree.elements[0].elements[0].elements[0].value, "Bar")
        self.assertEqual(tree.elements[1].elements[0].value, "Foo")  # ref attr `First Attr` in ref node `Second`
        self.assertEqual(tree.elements[1].elements[1].value, "Foo2")  # ref attr `Second Attr` in ref node `Second`
        self.assertEqual(tree.elements[2].elements[0].value, "Foo3")  # attr `Bar` in ref node `Third`


    def test_with_text_linked_tree(self):
        tree = Parser().parse('''treestructinfo "2.0"
                                 tree "linked_tree.tsinfo" as node "Linked Node"
                               end tree
                            ''')
        self.assertEqual(tree.elements[0].name, 'Linked Node')
        self.assertEqual(tree.elements[0].elements[0].name, 'Foo')
        self.assertEqual(tree.elements[0].elements[0].value, 'Bar')


    def test_with_tree_comment(self):
        tree = Parser().parse(''':: Main Comment
                                 ::
                                 :: Foo
                                 treestructinfo "2.0"
                                 end tree''')
        self.assertEqual(tree.comment, 'Main Comment\n\nFoo')

    def test_with_some_basic_comments(self):
        tree = tree = Parser().parse('''
                                 treestructinfo "2.0"
                                   ::
                                   :: Foo
                                   ::
                                   node Foo
                                     ::
                                     attr Bar "Bar"
                                   end node
                                 end tree''')
        self.assertEqual(tree.elements[0].comment, '\nFoo\n')
        self.assertEqual(tree.elements[0].elements[0].comment, '\n')
