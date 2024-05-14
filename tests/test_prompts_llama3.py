# Description: This file contains the code to test the prompt system with the llama3 model.
from typing import List, Union
from rich import inspect
from demo_prompts import multi_class
from demo_prompts import single_class
from demo_prompts import single_class_with_scoring
from demo_prompts.json_prompt_system import call_prompt


SERVICE_URL = "http://next-in-tech.fr:5005/v1/" # REMOTE
# SERVICE_URL = "http://localhost:5001/v1/" # LOCAL


def run_example(prompt_type: str, customer_feedback: str, themes :List[str])-> Union[multi_class.validation_model, single_class.validation_model, single_class_with_scoring.validation_model]:
    if prompt_type == "multi_class":
        user_prompt = multi_class.prompt_template
        validation_model = multi_class.validation_model
    elif prompt_type == "single_class":
        user_prompt = single_class.prompt_template
        validation_model = single_class.validation_model
    else:
        user_prompt = single_class_with_scoring.prompt_template
        validation_model = single_class_with_scoring.validation_model
    
    result = call_prompt(user_prompt=user_prompt, prompt_variables={"themes": themes, "input": customer_feedback}, validation_model=validation_model, service_url=SERVICE_URL)
    return result

def test_prompts_llama3_multi():
    result= run_example(prompt_type="multi_class", 
                        customer_feedback="The product is great, but the delivery was late.",
                        themes=["generic", "quality", "price", "customer service", "delivery", "product"])
    

    inspect(result) #type: ignore somehow mypy does not see the Output type
    assert isinstance(result, multi_class.validation_model)
def test_prompts_llama3_single():
    result = run_example(prompt_type="single_class",
                            customer_feedback="The product is great, but the delivery was late.",
                            themes=["generic", "quality", "price", "customer service", "delivery", "product"])
    inspect(result) #type: ignore somehow mypy does not see the Output 
    assert isinstance(result, single_class.validation_model)
def test_prompts_llama3_single_with_scoring():
    result = run_example(prompt_type="single_class_with_scoring",
                            customer_feedback="The product is great, but the delivery was late.",
                            themes=["generic", "quality", "price", "customer service", "delivery", "product"])
    inspect(result) #type: ignore somehow mypy does not see the Output
    assert isinstance(result, single_class_with_scoring.validation_model)