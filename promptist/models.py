from enum import StrEnum
from pydantic import BaseModel
from typing import List


class Prompt(BaseModel):
    text: str

    class Config:
        json_encoders = {
            StrEnum: lambda v: str(v)
        }


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

    class Config:
        json_encoders = {
            ChatRole: lambda v: v.value  # Serialize ChatRole as its value
        }


ChatAlias = List[Msg]


class PromptChat(Prompt):
    chat: ChatAlias

    def __str__(self):
        return f'{self.text}\n{self.chat}'

    class Config:
        json_encoders = {
            ChatRole: lambda v: v.value,  # Ensure roles serialize correctly
            Msg: lambda v: v.dict()  # Serialize messages as dicts
        }


    
