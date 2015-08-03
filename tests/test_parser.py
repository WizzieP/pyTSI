import unittest
import pyTSI.parser as parser


class ParserTest(unittest.TestCase):
    def test_with_one_ref_attr(self):
        tree = parser.parse(
            'treestructinfo "2.0"\nref attr Some Ref Attr\nend tree\nref attr Some Ref Attr "Some Value"')
        self.assertEqual(tree.elements[0].value, 'Some Value')

    def test_with_multiple_ref_attrs(self):
        tree = parser.parse('treestructinfo "2.0"\nref attr Some Ref Attr\nref attr Second \n'
                            'ref attr Third\nend tree\nref attr Some Ref Attr "Some Value"\n'
                            'ref attr Second "Second Value"\nref attr Third "Third Value"')
        self.assertEqual(tree.elements[0].value, 'Some Value')
        self.assertEqual(tree.elements[1].value, 'Second Value')
        self.assertEqual(tree.elements[2].value, 'Third Value')

    def test_with_one_ref_node(self):
        tree = parser.parse('treestructinfo "2.0"\nref node Some Node\nend tree\n'
                            'ref node Some Node\nattr Some Attr "Foo"\nend ref node')
        self.assertEqual(tree.elements[0].name, 'Some Node')
        self.assertEqual(tree.elements[0].elements[0].name, 'Some Attr')
        self.assertEqual(tree.elements[0].elements[0].value, 'Foo')

    def test_with_nested_ref_node(self):
        tree = parser.parse(''' treestructinfo "2.0"
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
        tree = parser.parse(''' treestructinfo "2.0"
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