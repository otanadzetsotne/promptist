# Promptist

## Overview
`promptist` is a Python package designed for managing and rendering 
structured prompt templates for chat-based interactions. It provides 
tools to structure, render, and format prompts and conversations 
with the use of placeholders and specific roles like `user`, `assistant`, 
and `system`. The package is highly extensible and supports dynamic 
placeholders in prompt files, making it easy to manage reusable 
templates for different chatbot scenarios.

## Installation

From PyPI:
```shell
pip install promptist
```

From source:
```shell
git clone https://github.com/otanadzetsotne/promptist.git
cd promptist
pip install .
```

## Key Features

### Renderer Class

The core functionality of `promptist` is provided by the `Renderer` class. It reads prompt files, replaces placeholders 
dynamically, and generates prompt conversations based on role-based chat structures. Below is a breakdown of its 
main functionalities:

1. **Initialization**:

    The `Renderer` class requires two parameters during initialization:
   
    * `name`: The name of the prompt file to render.
    * `prompts_dir`: The directory where the prompt files are located.
    
    Example:
    ```python
    renderer = Renderer(name='chat_scenario', prompts_dir='/path/to/prompts')
    ```

2. **Rendering Prompts**:

    The `render()` method reads the prompt template and replaces the placeholders defined in the prompt file with the data provided.
    Placeholders in the prompt files follow the `{type:name}` format. The supported types include:
    * `data`: Replaces the placeholder with the value provided in the data dictionary.
    * `include`: Includes another prompt template specified by name.
    
    Example:
    ```python
    rendered_prompt = renderer.render(data={"user_name": "Alice"})
    print(rendered_prompt.text)
    ```
   
3. **Chat Mode**:

    The `chat()` method structures the rendered prompt as a conversation between different roles (`system`, `user`, `assistant`).
    
    The prompt is parsed line by line to determine which role is speaking.

    Example:
    ```python
    chat_prompt = renderer.chat(data={"user_name": "Alice"})
    for message in chat_prompt.chat:
        print(message)
    ```

### Models

The package also defines several key models to structure and handle data in `promptist.models`.
* **Prompt**: A simple model representing a text-based prompt.
* **ChatRole**: An enumeration representing different roles in a chat, such as `system`, `user`, and `assistant`.
* **Msg**: A message model that contains the `role` and the `content` of the message.
* **PromptChat**: An extension of the `Prompt` model that includes a chat log, represented as a list of `Msg` objects.

These models make it easy to validate, parse, and display chat-based prompts in a structured way.

### Example of Prompt File Syntax

Prompt files are stored as `.txt` files within the specified directory. The placeholder format is `{type:name}`. Below is an example of how a prompt file might look:

`chat_scenario.txt`
```
system: Welcome to the chat service.
user: Hi, my name is {data:user_name}.
assistant: How can I assist you today, {data:user_name}?
```

### Including Other Prompts

You can include other prompts by using the `include` type in placeholders. For example:
```
system: {include:welcome.system_welcome}
user: {data:user_message}
```
In this case, the `welcome/system_welcome.txt` file will be included where `{include:welcome.system_welcome}` is placed.

### Placeholder Syntax
* **Data Placeholder**: `{data:name}` replaces the placeholder with the value of `name` in the provided data dictionary.
* **Include Placeholder**: `{include:filename}` includes the contents of another prompt file located in the `prompts` directory.

## Example Usage

```python
from promptist.renderer import Renderer

# Initialize Renderer
renderer = Renderer(name='chat_scenario', prompts_dir='./prompts')

# Render prompt with data
data = {
    'user_name': 'Alice',
}
rendered_prompt = renderer.render(data)
print(rendered_prompt.text)

# Render chat-based prompt
chat_prompt = renderer.chat(data)
for message in chat_prompt.chat:
    print(message.role, ":", message.content)
```

## License
This project is licensed under the MIT License. For more information, see the [LICENSE](https://github.com/otanadzetsotne/promptist/LICENSE) file.

## Author
### **Tsotne Otanadze**

For questions, issues, or contributions, feel free to contact me at: [otanadzetsotne@yahoo.com](mailto:otanadzetsotne@yahoo.com).

If you use this repository in your projects, please note it in the project description or leave a [link](https://github.com/otanadzetsotne/promptist) to this repository. I will be glad to any feedback and suggestions!
