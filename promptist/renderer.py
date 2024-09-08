import os
import re
from functools import partial

from models import Prompt, PromptChat, ChatRole, Msg, ChatAlias


rgx_placeholder = re.compile(r'(?P<placeholder>{(?P<type>\w+):(?P<name>[\w.]+)})', re.IGNORECASE | re.MULTILINE)
rgx_cleaner = re.compile(r'[^\w\s]', re.IGNORECASE | re.MULTILINE)


class Renderer:
    roles = {role.value for role in ChatRole}  # Create a set of role values for quick lookup

    def __init__(self, name: str = None, prompts_dir: str = None):
        # Define prompts directory
        if prompts_dir is None:
            raise RuntimeError
        prompts_dir = os.path.abspath(prompts_dir)
        if not os.path.exists(prompts_dir) or not os.path.isdir(prompts_dir):
            raise FileNotFoundError(f'Prompts directory: {prompts_dir}')
        self.prompts_dir = prompts_dir

        # Define prompt path
        self.name = name
        self.file_name = f'{self.name.replace('.', '/')}.txt'
        self.path = os.path.join(self.prompts_dir, self.file_name)

    def _read_template(self):
        with open(self.path, 'r') as file:
            return file.read()

    def _format_placeholder_match(self, rgx_match, data):
        placeholder = rgx_match.groupdict()
        match placeholder.get('type'):
            case 'include':
                template = placeholder.get('name')
                template = data.get(template, template)
                return Renderer(template, self.prompts_dir).render(data=data).text
            case 'data':
                key = placeholder.get('name', '')
                value = str(data.get(key, ''))
                return value
            case _:
                raise KeyError(f'{self.name}: placeholder type error "{placeholder.get('placeholder')}"')

    def render(self, data: dict | None = None) -> Prompt:
        try:
            formatter = partial(self._format_placeholder_match, data=data)
            template = self._read_template()
            prompt = rgx_placeholder.sub(formatter, template)
            prompt = Prompt(text=prompt)
            return prompt
        except Exception as e:
            print(f'{self.name}: {e}')
            raise e

    def chat(self, data: dict | None = None) -> PromptChat:
        chat: ChatAlias = []
        role: ChatRole | None = None
        message = ''

        prompt_text: str = self.render(data).text
        for line in prompt_text.split('\n'):
            line_stripped: str = line.strip()
            role_str: str = line_stripped[:-1].lower()
            if role_str in self.roles:
                if role is not None:
                    chat.append(Msg(role=role, content=message.strip()))

                try:
                    role = ChatRole(role_str)
                except ValueError:
                    continue  # Skip lines with invalid roles
                message = ''
            else:
                message += f'{line}\n'

        if role is not None:
            chat.append(Msg(role=role, content=message.strip()))

        return PromptChat(text=prompt_text, chat=chat)

    @staticmethod
    def clean_input(input_string):
        """
        Sanitizes user input to prevent injection attacks or unintended execution of code.
        This function can be extended based on specific sanitization needs.

        Parameters:
        - input_string: The user-generated string to be sanitized.

        Returns:
        - A sanitized version of the input string.
        """
        # Example: Escaping potentially dangerous characters
        # This can be customized based on the context and specific security requirements
        cleaned_string = rgx_cleaner.sub('', input_string)
        return cleaned_string
