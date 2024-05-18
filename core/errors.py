class TemplateNotFoundError(Exception):
    def __init__(self, template: str):
        self.message = f'Template {template!r} not found'
        self.template = template

    def __repr__(self) -> str:
        return self.message
    
    __str__ = __repr__
