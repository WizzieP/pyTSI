from pyTSI.elements import TSIException
from pyTSI.parser import parse


class TSI:
    def __init__(self, source):
        self._tree = parse(source)

    def get_attr(self, target):
        """Returns the attribute's value. The attribute is always the last element in the path, the earlier are nodes
        :param target: Path to the attribute, divided by dots (`.`). The last element must be an attribute while others
                        must be nodes
        :return: String value of the attribute or None if the attribute can not be found or the path is broken
        """
        current_node = self._tree
        targets = target.split('.')
        try:
            for name in targets[:-1]:
                current_node = current_node.get(name)
            attr = current_node.get(targets[-1])
            return attr.value
        except (TSIException, AttributeError) as e:
            return None


def load(source):
    return TSI(source)