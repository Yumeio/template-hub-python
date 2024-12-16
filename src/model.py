from typing import List, Optional

class ModelDeclaration():
    def __init__(
        self, 
        filename: str, 
        **kwargs
    ):
        self.filename = filename
        for key, value in kwargs.items():
            setattr(self, key, value)
        
class ModelInfo():
    def __init__(
        self, 
        model_id: str,
        model_name: str,
        model_description: str,
        model_tags: List[str] = [],
        model_pipeline: List[str] = [],
        model_dependencies: List[str] = [],
        model_declaration: Optional[ModelDeclaration] = None,
        **kwargs,
    ):
        self.model_id = model_id
        self.model_name = model_name
        self.model_description = model_description
        self.model_tags = model_tags
        self.model_pipeline = model_pipeline
        self.model_dependencies = model_dependencies
        self.model_declaration = model_declaration
        for key, value in kwargs.items():
            setattr(self, key, value)