from textwrap import dedent
import subprocess
import sys
import os


def write_tmp(tmp_path, name, text):
    path = tmp_path / (name.replace('.', '/') + '.txt')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text))
    return path


def run_cli(args, cwd=None):
    return subprocess.run([sys.executable, '-m', 'promptist.cli', *args], capture_output=True, text=True, cwd=cwd)


def test_cli_render(tmp_path):
    write_tmp(tmp_path, 'a.b', """
    user: Hi {data:name}
    """
    )
    res = run_cli(['render', '--name', 'a.b', '--prompts-dir', str(tmp_path), '--data', '{"name":"Ann"}'])
    assert res.returncode == 0
    assert 'Hi Ann' in res.stdout


def test_cli_validate_fail(tmp_path):
    write_tmp(tmp_path, 'bad.t', """
    system: {include:not.exist}
    """)
    res = run_cli(['validate', '--name', 'bad.t', '--prompts-dir', str(tmp_path)])
    assert res.returncode != 0
    assert 'ERROR' not in res.stderr


