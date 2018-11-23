class treeNode:
    def __init__(self, data, code):
        self.data = data
        self.code = code
        self.children = []


    def addChild(self, child):
        self.children.append(child)
