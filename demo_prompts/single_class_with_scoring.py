
from pydantic import BaseModel, ConfigDict

class SingleClassModelWithScoring(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                
                {
                    "feedback": "I love this product, it's amazing!",
                    "theme": "generic",
                    "tonality": 10
                  
                }
                
          
            ]
        }
    )
    feedback: str
    theme: str
    tonality: int

validation_model=SingleClassModelWithScoring
prompt_template ="""
### Instructions:

Use the list of themes provided below to determine the appropriate theme.


[THEMES]
Striclty use this list of themes.
{themes}

[SENTIMENT]
tonality: a grade from 0 to 10 where 10 is the most positive and 0 the most negative. Put the grade in the "tonality" property.
Always use a number between 0 and 10, and 5 if the tone is neutral.

### USER FEEDBACK: {input}

[OUTPUT FORMAT]
Format the object like in the example below. 
{format_instructions}
"""


validation_code = """
class SingleClassModel(BaseModel):
    feedback: str
    theme: str
    tonality: int
"""