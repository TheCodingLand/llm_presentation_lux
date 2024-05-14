from typing import List
from pydantic import BaseModel, ConfigDict

class FeedbackItem(BaseModel):

    feedback: str
    theme: str
    tonality: int

class MultiClassModelWithScoring(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "feedbacks": [
                        {
                            "feedback": "I love this product, it's amazing!",
                            "theme": "product",
                            "tonality": 10
                        },
                        {
                            "feedback": "the delivery was late",
                            "theme": "delivery",
                            "tonality": 3
                        }
                    ]
                }
            ]
        }
    )
    feedbacks: List[FeedbackItem]



validation_model=MultiClassModelWithScoring
prompt_template = """
### Instructions:

Use the list of themes provided below to determine the appropriate theme.
Split the comment touching different themes into separate "feedback" properties.

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
class FeedbackItem(BaseModel):
    feedback: str
    theme: str
    tonality: int

class MultiClassModelWithScoring(BaseModel):
    feedbacks: List[FeedbackItem]
"""