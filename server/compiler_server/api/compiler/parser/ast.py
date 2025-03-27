class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def __str__(self):
        base = self.type
        if self.value:
            base += f"({self.value})"
        if self.children:
            children_str = ', '.join(str(child) for child in self.children)
            return f"{base}[{children_str}]"
        return base