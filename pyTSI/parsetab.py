
# C:\Users\Andrzej\Projects\pyTSI2\pyTSI\parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = 'F50DAEA7D0E540326D9C13C791BB62F4'
    
_lr_action_items = {'$end':([3,10,29,30,38,40,41,42,48,51,53,],[0,-1,-2,-19,-22,-20,-21,-13,-14,-23,-24,]),'NODE':([4,5,9,11,12,13,14,18,27,32,33,34,36,42,44,48,49,50,],[7,-5,-6,-7,-8,-10,-9,-11,7,-12,-17,-16,-25,-13,-15,-14,-26,7,]),'REF_NODE_NAME':([16,37,],[24,46,]),'END_NODE':([5,9,11,12,13,14,18,27,32,33,34,36,42,44,48,49,],[-5,-6,-7,-8,-10,-9,-11,35,-12,-17,-16,-25,-13,-15,-14,-26,]),'IN_MODE':([36,],[45,]),'ATTR':([4,5,9,11,12,13,14,18,27,32,33,34,36,42,44,48,49,50,],[15,-5,-6,-7,-8,-10,-9,-11,15,-12,-17,-16,-25,-13,-15,-14,-26,15,]),'REF_NODE':([4,5,9,11,12,13,14,18,27,29,30,32,33,34,36,38,40,41,42,44,48,49,50,51,53,],[16,-5,-6,-7,-8,-10,-9,-11,16,37,-19,-12,-17,-16,-25,-22,-20,-21,-13,-15,-14,-26,16,-23,-24,]),'TREE':([4,5,9,11,12,13,14,18,27,32,33,34,36,42,44,48,49,50,],[8,-5,-6,-7,-8,-10,-9,-11,8,-12,-17,-16,-25,-13,-15,-14,-26,8,]),'REF_ATTR':([4,5,9,11,12,13,14,18,27,29,30,32,33,34,36,38,40,41,42,44,48,49,50,51,53,],[17,-5,-6,-7,-8,-10,-9,-11,17,39,-19,-12,-17,-16,-25,-22,-20,-21,-13,-15,-14,-26,17,-23,-24,]),'END_TREE':([4,5,9,11,12,13,14,18,32,33,34,36,42,44,48,49,],[10,-5,-6,-7,-8,-10,-9,-11,-12,-17,-16,-25,-13,-15,-14,-26,]),'NEWLINES':([1,6,10,20,22,24,25,26,31,35,43,46,52,],[5,-3,-18,5,30,33,34,-4,42,44,48,5,53,]),'AS_NODE':([21,],[28,]),'TSINFO':([0,],[2,]),'REF_ATTR_NAME':([17,39,],[25,47,]),'END_REF_NODE':([5,9,11,12,13,14,18,32,33,34,36,42,44,48,49,50,],[-5,-6,-7,-8,-10,-9,-11,-12,-17,-16,-25,-13,-15,-14,-26,52,]),'ATTR_NAME':([15,],[23,]),'VALUE':([2,8,19,23,28,32,42,45,47,48,49,51,],[6,21,26,31,36,43,-13,31,31,-14,43,43,]),'NODE_NAME':([7,],[20,]),'TREE_NAME':([6,],[19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'refNodeDeclaration':([4,27,50,],[13,13,13,]),'refsElementList':([22,],[29,]),'elementList':([1,20,46,],[4,27,50,]),'refNodeDefinition':([29,],[38,]),'refAttrDeclaration':([4,27,50,],[14,14,14,]),'treeheader':([0,],[1,]),'element':([4,27,50,],[9,9,9,]),'valueList':([23,45,47,],[32,49,51,]),'linkedTree':([4,27,50,],[18,18,18,]),'attr':([4,27,50,],[11,11,11,]),'seen_END_TREE':([10,],[22,]),'refElement':([29,],[40,]),'tree':([0,],[3,]),'refAttrDefinition':([29,],[41,]),'node':([4,27,50,],[12,12,12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> tree","S'",1,None,None,None),
  ('tree -> treeheader elementList END_TREE','tree',3,'p_tree','parser.py',14),
  ('tree -> treeheader elementList END_TREE seen_END_TREE refsElementList','tree',5,'p_tree','parser.py',15),
  ('treeheader -> TSINFO VALUE','treeheader',2,'p_treeheader','parser.py',19),
  ('treeheader -> TSINFO VALUE TREE_NAME VALUE','treeheader',4,'p_treeheader','parser.py',20),
  ('elementList -> NEWLINES','elementList',1,'p_elementList_empty','parser.py',25),
  ('elementList -> elementList element','elementList',2,'p_elementList_nonempty','parser.py',29),
  ('element -> attr','element',1,'p_element','parser.py',34),
  ('element -> node','element',1,'p_element','parser.py',35),
  ('element -> refAttrDeclaration','element',1,'p_element','parser.py',36),
  ('element -> refNodeDeclaration','element',1,'p_element','parser.py',37),
  ('element -> linkedTree','element',1,'p_element','parser.py',38),
  ('attr -> ATTR ATTR_NAME valueList','attr',3,'p_attr','parser.py',42),
  ('valueList -> VALUE NEWLINES','valueList',2,'p_valueList_single','parser.py',46),
  ('valueList -> valueList VALUE NEWLINES','valueList',3,'p_valueList_multiple','parser.py',50),
  ('node -> NODE NODE_NAME elementList END_NODE NEWLINES','node',5,'p_node','parser.py',55),
  ('refAttrDeclaration -> REF_ATTR REF_ATTR_NAME NEWLINES','refAttrDeclaration',3,'p_refAttrDeclaration','parser.py',59),
  ('refNodeDeclaration -> REF_NODE REF_NODE_NAME NEWLINES','refNodeDeclaration',3,'p_refNodeDeclaration','parser.py',65),
  ('seen_END_TREE -> <empty>','seen_END_TREE',0,'p_seen_END_TREE','parser.py',71),
  ('refsElementList -> NEWLINES','refsElementList',1,'p_refsElementList_empty','parser.py',77),
  ('refsElementList -> refsElementList refElement','refsElementList',2,'p_refsElementList_nonempty','parser.py',80),
  ('refElement -> refAttrDefinition','refElement',1,'p_refElement','parser.py',83),
  ('refElement -> refNodeDefinition','refElement',1,'p_refElement','parser.py',84),
  ('refAttrDefinition -> REF_ATTR REF_ATTR_NAME valueList','refAttrDefinition',3,'p_refAttrDefinition','parser.py',89),
  ('refNodeDefinition -> REF_NODE REF_NODE_NAME elementList END_REF_NODE NEWLINES','refNodeDefinition',5,'p_refNodeDefinition','parser.py',95),
  ('linkedTree -> TREE VALUE AS_NODE VALUE','linkedTree',4,'p_linkedTree_simple','parser.py',103),
  ('linkedTree -> TREE VALUE AS_NODE VALUE IN_MODE valueList','linkedTree',6,'p_linkedTree_extended','parser.py',109),
]
