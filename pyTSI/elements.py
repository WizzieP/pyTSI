class Attr:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value


class Node:
    def __init__(self, name, elements=None, ref=False, link_file_name=None):
        self.name = name
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
        self.link_file_name = link_file_name

    def get(self, name):
        for element in self.elements:
            if element.name == name:
                return element
        else:
            raise TSIException('Element with name: ' + name + ' not found')



class TSIException(Exception):
    pass