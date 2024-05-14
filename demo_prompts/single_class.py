
from pydantic import BaseModel, ConfigDict

class SingleClassModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                
                {
                    "feedback": "I love this product, it's amazing!",
                    "theme": "generic",
                  
                }
                
          
            ]
        }
    )
    feedback: str
    theme: str

validation_model=SingleClassModel
prompt_template = """
### Instructions:

Use the list of themes provided below to determine the appropriate theme.
if it is a long sentence, chose the closest theme to the main idea of the feedback.

[THEMES]
Striclty use this list of themes.
{themes}

### USER FEEDBACK: {input}

[OUTPUT FORMAT]
Format the object like in the example below. 
{format_instructions}
"""



validation_code = """
class SingleClassModel(BaseModel):
    feedback: str
    theme: str
"""
