from typing import List, cast
from demo_prompts import multi_class
from demo_prompts import single_class
from demo_prompts import single_class_with_scoring
from demo_prompts.gradio_utils import prepare_output_for_gradio_highlighted_text
from demo_prompts.json_prompt_system import call_prompt, PromptSystem

base_themes = ["generic", "quality", "price", "customer service", "delivery", "product"]

demo_prompts = {
    "multi_class": multi_class.prompt_template,
    "single_class": single_class.prompt_template,
    "single_class_with_scoring": single_class_with_scoring.prompt_template,
}

def test_get_prompt_multi_class():
    ps = PromptSystem(user_prompt=multi_class.prompt_template, system_prompt="Zero Shot Classification", validation_model=multi_class.validation_model, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, api_call_method=call_prompt, service_url="http://next-in-tech.fr:5005/v1/")
    formated_prompt= ps.build_prompt()
    assert isinstance(formated_prompt, str)

def test_get_prompt_single_class():
    ps = PromptSystem(user_prompt=single_class.prompt_template, system_prompt="Zero Shot Classification", validation_model=single_class.validation_model, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, api_call_method=call_prompt, service_url="http://next-in-tech.fr:5005/v1/")
    formated_prompt= ps.build_prompt()
    assert isinstance(formated_prompt, str)

def test_get_prompt_single_class_with_scoring():
    ps = PromptSystem(user_prompt=single_class_with_scoring.prompt_template, system_prompt="Zero Shot Classification", validation_model=single_class_with_scoring.validation_model, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, api_call_method=call_prompt, service_url="http://next-in-tech.fr:5005/v1/")
    formated_prompt= ps.build_prompt()
    assert isinstance(formated_prompt, str)

def test_call_prompt_multi_class():
    result = call_prompt(user_prompt=multi_class.prompt_template, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, validation_model=multi_class.validation_model, service_url="http://next-in-tech.fr:5005/v1/")
    assert isinstance(result, multi_class.validation_model)

def test_call_prompt_single_class():

    result = call_prompt(user_prompt=single_class.prompt_template, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, validation_model=single_class.validation_model, service_url="http://next-in-tech.fr:5005/v1/")
    assert isinstance(result, single_class.validation_model)

def test_call_prompt_single_class_with_scoring():
    result = call_prompt(user_prompt=single_class_with_scoring.prompt_template, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, validation_model=single_class_with_scoring.validation_model, service_url="http://next-in-tech.fr:5005/v1/")
    assert isinstance(result, single_class_with_scoring.validation_model)

def test_prepare_output_for_gradio_highligted_text_multi_class():
    output = call_prompt(user_prompt=multi_class.prompt_template, prompt_variables={"themes": base_themes, "input": "The product is great, but the delivery was late."}, validation_model=multi_class.validation_model, service_url="http://next-in-tech.fr:5005/v1/")
    result = prepare_output_for_gradio_highlighted_text(output)
    assert result[0][1] in base_themes

