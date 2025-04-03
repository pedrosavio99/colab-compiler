class ASTNode:
    def __init__(self, type, value=None, id=None, children=None):
        self.type = type
        self.value = value
        self.id = id
        self.children = children or []

    def __str__(self):
        return f"ASTNode(type={self.type}, value={self.value}, id={self.id}, children={self.children})"