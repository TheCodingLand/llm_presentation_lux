from typing import List, cast
from demo_prompts import multi_class, single_class, single_class_with_scoring


def prepare_output_for_gradio_highlighted_text(output: multi_class.validation_model| single_class_with_scoring.validation_model| single_class.validation_model) -> List[List[str]]:
    hightlighted_text_data : List[List[str]] = []
    if isinstance(output, single_class.validation_model) or isinstance(output, single_class_with_scoring.validation_model):
        return [[output.feedback, output.theme]]
    output = cast(multi_class.validation_model| single_class_with_scoring.validation_model, output) # type: ignore
    
    for feedback in output.feedbacks: #type: ignore
        feedback = cast(multi_class.FeedbackItem,feedback)
        hightlighted_text_data.append([feedback.feedback, feedback.theme])
    return hightlighted_text_data