import os
from functools import partial

from promptist.models import Prompt, PromptChat, ChatRole, Msg, ChatAlias
from promptist.constants import RGX_PLACEHOLDER, RGX_CLEANER


 


class Renderer:
    roles = {role.value for role in ChatRole}  # Create a set of role values for quick lookup

    def __init__(self, name: str = None, prompts_dir: str = None):
        if not prompts_dir:
            raise ValueError("prompts_dir must be provided and not be empty.")
        if not name:
            raise ValueError("name must be provided and not be empty.")

        self.prompts_dir = os.path.abspath(prompts_dir)
        self.name = name

        if not os.path.isdir(self.prompts_dir):
            raise FileNotFoundError(f'Prompts directory not found: {self.prompts_dir}')

        # Define prompt path
        file_name = self.name.replace('.', '/')
        file_name = f'{file_name}.txt'
        self.file_name = file_name
        self.path = os.path.join(self.prompts_dir, self.file_name)

        if not os.path.exists(self.path):
            raise FileNotFoundError(f'Prompt file not found: {self.path}')

    def _read_template(self):
        with open(self.path, 'r') as file:
            return file.read()

    def _format_placeholder_match(self, match, data):
        placeholder_type = match.group('type')
        placeholder_name = match.group('name')
        placeholder_full = match.group('placeholder')
        match placeholder_type:
            case 'include':
                template = data.get(placeholder_name, placeholder_name)
                return Renderer(template, self.prompts_dir).render(data=data).text
            case 'data':
                return str(data.get(placeholder_name, ''))
            case _:
                raise KeyError(f'Unsupported placeholder type in {self.name}: {placeholder_full}')

    def render(self, data: dict | None = None) -> Prompt:
        if data is None:
            data = {}
        try:
            template = self._read_template()
            formatter = partial(self._format_placeholder_match, data=data)
            prompt_text = RGX_PLACEHOLDER.sub(formatter, template)
            return Prompt(text=prompt_text)
        except Exception as e:
            raise RuntimeError(f'Error rendering template {self.name}: {e}') from e

    def chat(self, data: dict | None = None) -> PromptChat:
        if data is None:
            data = {}
        prompt_text = self.render(data).text
        chat: ChatAlias = []
        role: ChatRole | None = None
        message = ''

        for line in prompt_text.split('\n'):
            line_stripped = line.strip()

            # Try to detect a role prefix of the form "<role>: <content>"
            if ':' in line_stripped:
                candidate, rest = line_stripped.split(':', 1)
                candidate_lower = candidate.strip().lower()
                if candidate_lower in self.roles:
                    # Flush previous accumulated message
                    if role is not None:
                        chat.append(Msg(role=role, content=message.strip()))
                    try:
                        role = ChatRole(candidate_lower)
                    except ValueError:
                        role = None
                        message = ''
                        continue
                    # Start a new message with inline content after the colon (if any)
                    message = rest.lstrip()
                    continue

            # Not a role header line; accumulate into current message if a role is active
            if role is not None:
                if message:
                    message += f'\n{line}'
                else:
                    message = line

        if role:
            chat.append(Msg(role=role, content=message.strip()))

        return PromptChat(text=prompt_text, chat=chat)

    @staticmethod
    def clean_input(input_string):
        return RGX_CLEANER.sub('', input_string)


if __name__ == '__main__':
    print('OK.')
