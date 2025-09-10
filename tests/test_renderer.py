import os
from textwrap import dedent

import pytest

from promptist.renderer import Renderer
from promptist.validation import validate_template_text


def write_tmp(tmp_path, name, text):
    path = tmp_path / (name.replace('.', '/') + '.txt')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text))
    return path


def test_render_and_chat(tmp_path):
    write_tmp(tmp_path, 'chat.scenario', """
    system: Hello
    user: Hi {data:name}
    assistant: How can I help?
    """)
    r = Renderer(name='chat.scenario', prompts_dir=str(tmp_path))
    out = r.render({'name': 'Alice'})
    assert 'Hi Alice' in out.text
    chat = r.chat({'name': 'Alice'})
    assert len(chat.chat) == 3
    assert chat.chat[1].content == 'Hi Alice'


def test_include(tmp_path):
    write_tmp(tmp_path, 'greet.base', """
    user: Hello {data:name}
    """)
    write_tmp(tmp_path, 'greet.main', """
    system: {include:greet.base}
    """)
    r = Renderer(name='greet.main', prompts_dir=str(tmp_path))
    text = r.render({'name': 'Bob'}).text
    assert 'Hello Bob' in text


def test_validation_reports_missing_include(tmp_path):
    write_tmp(tmp_path, 'bad.template', """
    system: {include:missing.part}
    """)
    path = os.path.join(str(tmp_path), 'bad/template.txt')
    with open(path) as f:
        report = validate_template_text(f.read(), prompts_dir=str(tmp_path))
    assert not report.is_valid
    assert any('Included template not found' in i.message for i in report.issues)


