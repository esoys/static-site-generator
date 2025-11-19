class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        

    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if not self.props:
            return ""
        full_string = ""
        for props in self.props:
            full_string += f' {props}="{self.props[props]}"'
        return full_string


    def __repr__(self):
        return f"HTMLNode:\n - tag: {self.tag}\n - value: {self.value}\n - children: {self.children}\n - props: {self.props}"




class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
        self.full_props = super().props_to_html()

    def to_html(self):
        value = "" if self.value is None else self.value

        if not self.tag:
            return value

        return f'<{self.tag}{self.full_props}>{self.value}</{self.tag}>'



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)
        self.full_props = super().props_to_html() if self.props else ""


    def to_html(self):
        if not self.tag:
            raise ValueError

        if not self.children:
            raise ValueError
        
        children = ""
        for child in self.children:
            children += child.to_html()

        return f'<{self.tag}{self.full_props}>{children}</{self.tag}>'



