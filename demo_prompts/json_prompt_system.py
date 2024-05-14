import logging
from typing import Any, Callable, Dict, Generic, Type, TypeVar

from pydantic import BaseModel
from typing import Type, TypeVar
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
system_prompt = "You are an assistant who attempts to answer the user's task. you only return json data."
prompt_per_model_type= {
     "llama3": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n",
     "dolphin": "<|im_start|>system<|im_end|>\n{system_prompt}<|im_start|>user<|im_end|>\n{user_prompt}<|im_start|>assistant<|im_end|>\n",
     "llama2": "[INST] {system_prompt}\n[/INST] {user_prompt}\n"
}


def call_api_with_prompt(service_url: str, model: str, prompt: str) -> str:
    client = OpenAI(
        api_key="sk-1234567890abcdef1234567890abcdef",
        base_url=service_url,
    )
    completion: ChatCompletion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False,
        max_tokens=2000,
        temperature=0.0,
    )
    output = str(
        completion.choices[0].message.content
    )

    return output

T = TypeVar("T", bound=BaseModel)

class PromptSystem(Generic[T]):
    def __init__(self, user_prompt: str, system_prompt: str, validation_model: Type[T], prompt_variables: Dict[str, Any], api_call_method: Callable[[str, str, str], str], service_url: str, model_prompt_style: str = "llama3", model: str = "llama3:instruct") -> None:
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        self.validation_model = validation_model
        self.prompt_variables = prompt_variables
        self.api_call_method = api_call_method
        self.model_prompt_style = model_prompt_style
        self.service_url = service_url
        self.model=model
        # verify that prompt template has all the correct variables:
        for key in prompt_variables.keys():
            if key not in user_prompt:
                raise ValueError(f"Prompt template missing variable {key}")
            

    def build_prompt(self) -> str:

        return prompt_per_model_type[self.model_prompt_style].format(system_prompt=self.system_prompt, user_prompt=self.user_prompt)

    
    def format_prompt(self) -> None:
        if 'examples' not in self.validation_model.model_config.get("json_schema_extra", {}).keys(): #type: ignore
            logging.warning(f'Output model does not have "examples" key in json_schema_extra using jsonschema instead')
            validation_prompt_text = f"Use the following jsonschema object definition to validate the output: \n\n```json\n{self.validation_model.model_json_schema()}\n```"
            self.user_prompt = self.user_prompt.format(**self.prompt_variables, format_instructions=validation_prompt_text)
        else:
            self.user_prompt = self.user_prompt.format(**self.prompt_variables, format_instructions=self.validation_model.model_config.get("json_schema_extra").get("examples")[0]) #type: ignore
    
    def __str__(self) -> str:
        self.format_prompt()

        return self.build_prompt()
    
    def validate_output(self, output: str) -> T:
        return self.validation_model.model_validate_json(output)
    
    def call_prompt_with_retries(self) -> T:
        prompt = self.__str__()
        result : str = self.api_call_method(self.service_url, self.model, prompt)
        
        return self.validate_output(result)
        

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.call_prompt_with_retries()

def call_prompt(user_prompt: str, prompt_variables: Dict[str, Any], validation_model: Type[T], api_call_method: Callable[[str, str], Any]= call_api_with_prompt, model_prompt_style: str = "llama3", service_url: str="http://next-in-tech.fr:5005/v1/", model: str ='llama3:instruct') -> T:
    result: T = PromptSystem(user_prompt=user_prompt, 
                                                system_prompt=system_prompt, 
                                                validation_model=validation_model, 
                                                prompt_variables=prompt_variables, 
                                                api_call_method=api_call_method, 
                                                model_prompt_style=model_prompt_style,
                                                service_url=service_url,
                                                model=model
                                                )()
    return result                           

