from typing import List
from enum import StrEnum
from pydantic import BaseModel


class Prompt(BaseModel):
    text: str


class ChatRole(StrEnum):
    system = 'system'
    user = 'user'
    assistant = 'assistant'

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'\'{self.__str__()}\''


class Msg(BaseModel):
    role: ChatRole
    content: str

    def __str__(self):
        return '\\n'.join(f'{self.role}: {self.content}'.split('\n'))

    def __repr__(self):
        return f'\'{self.__str__()}\''


ChatAlias = List[Msg]


class PromptChat(Prompt):
    chat: ChatAlias

    def __str__(self):
        return f'{self.text}\n{self.chat}'
