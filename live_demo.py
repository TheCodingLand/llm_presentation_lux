
from typing import Dict, List, Tuple, Type
import gradio as gr
from demo_prompts import multi_class
from demo_prompts.single_class import SingleClassModel
from demo_prompts.single_class_with_scoring import SingleClassModelWithScoring
from demo_prompts.multi_class import MultiClassModelWithScoring
from demo_prompts import single_class
from demo_prompts import single_class_with_scoring
from demo_prompts.gradio_utils import prepare_output_for_gradio_highlighted_text
from demo_prompts.json_prompt_system import call_prompt, PromptSystem, system_prompt

SERVICE_URL = "https://llama.next-in-tech.fr/v1/"
allowed_models = ["llama3:instruct", "taozhiyuai/llama-3-aplite-instruct-4x8b-gguf-moe:q6k"]
#MODEL = "llama3:instruct"
#SERVICE_URL = "http://localhost:5001/v1/" # LOCAL
#SERVICE_URL = "http://localhost:11434/v1/" # container

base_themes : List[str] = ["generic", "quality", "price", "customer service", "delivery", "product", "website"]

default_prompt_key = "single_class"
demo_prompts : Dict[str, str] = {
    "multi_class": multi_class.prompt_template,
    "single_class": single_class.prompt_template,
    "single_class_with_scoring": single_class_with_scoring.prompt_template,
}
demo_validation_code : Dict[str, str] = {
    "multi_class": multi_class.validation_code,
    "single_class": single_class.validation_code,
    "single_class_with_scoring": single_class_with_scoring.validation_code,
}

demo_validation_models: Dict[str, Type[SingleClassModel] | Type[SingleClassModelWithScoring]| Type[MultiClassModelWithScoring] ] = {
    "multi_class": MultiClassModelWithScoring,
    "single_class": SingleClassModel,
    "single_class_with_scoring": SingleClassModelWithScoring
}

def fake_api_call_method(service_url: str, model: str, prompt: str) -> str: # linter happiness
    return ""

def get_formated_prompt(user_prompt: str, themes: List[str], prompt_key: str = default_prompt_key) -> str:
    ps = PromptSystem(user_prompt=demo_prompts[prompt_key], system_prompt=system_prompt, validation_model=demo_validation_models[prompt_key], prompt_variables={"themes": themes, "input": user_prompt}, api_call_method=fake_api_call_method, service_url=SERVICE_URL)
    return str(ps)

def get_validation_code(prompt_key: str = default_prompt_key) -> str:
    return demo_validation_code[prompt_key]
    

def call_prompt_action(user_prompt: str, themes: List[str], prompt_key: str, model: str) -> Tuple[str, List[List[str]], str]:
    result = call_prompt(user_prompt=demo_prompts[prompt_key], prompt_variables={"themes": themes, "input": user_prompt}, validation_model=demo_validation_models[prompt_key], service_url=SERVICE_URL, model=model)
    return result.model_dump_json(indent=4), prepare_output_for_gradio_highlighted_text(result), get_formated_prompt(user_prompt, themes, prompt_key)

def create_app() -> gr.Blocks:
    with gr.Blocks(title="Live Demo Zero Shot Classification", css="footer {visibility: hidden}") as app:
        #Add a title to the app
        gr.Markdown("# Live Demo Zero Shot Classification")

        gr.Markdown("### Themes")
        themes = base_themes.copy()
        with gr.Row():

            themes_input = gr.Dropdown(choices=themes, label="Themes", allow_custom_value=True, multiselect=True, max_choices=99, min_width=400)
            
            customer_feedback = gr.Textbox(label="Customer Feedback", placeholder="Enter the customer feedback here", lines=5, min_width=400)
            prompt_key = gr.Dropdown(label="Prompt type", choices=["multi_class", "single_class", "single_class_with_scoring"], value=default_prompt_key, allow_custom_value=False, min_width=150)
            model = gr.Dropdown(label="Model", value=allowed_models[0],choices=allowed_models, allow_custom_value=False, min_width=150)
            pydantic_validation_model = gr.Code(get_validation_code(default_prompt_key), language="python", label="Pydantic Validation Model", lines=10, min_width=400)
        
        formated_prompt = gr.Markdown("", label="Formated Prompt")
        format_prompt= gr.Button("Format Prompt")
        prompt_key.change(fn=get_validation_code, inputs=[prompt_key], outputs=[pydantic_validation_model]) # type: ignore
        format_prompt.click(fn=get_formated_prompt, inputs=[customer_feedback, themes_input, prompt_key], outputs=[formated_prompt]) # type: ignore
        hightlighted_text_data = []
        colors = [ "blue", "green", "yellow", "red", "purple", "orange", "pink", "brown", "gray", "black"][0:len(base_themes)]
        color_map = {theme: color for theme, color in zip(base_themes, colors)}
        highlighted_text_for_each_feedback = gr.gradio.HighlightedText(hightlighted_text_data, color_map=color_map)

        output = gr.Code(language="json", label="Output", lines=10, min_width=400)
        button = gr.Button("Submit")
        button.click(fn=call_prompt_action, inputs=[customer_feedback, themes_input, prompt_key, model], outputs=[output, highlighted_text_for_each_feedback, formated_prompt]) # type: ignore
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch() # type: ignore

