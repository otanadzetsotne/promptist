import argparse
import json
import os
import sys
from typing import Any

from promptist.renderer import Renderer
from promptist.validation import validate_template_file, validate_template_text


def _load_data(data_arg: str | None) -> dict[str, Any]:
    if not data_arg:
        return {}
    # If starts with '@', treat as path to JSON file
    if data_arg.startswith('@'):
        path = data_arg[1:]
        with open(path, 'r') as f:
            return json.load(f)
    # else try parse as JSON literal
    return json.loads(data_arg)


def cmd_render(args: argparse.Namespace) -> int:
    data = _load_data(args.data)
    renderer = Renderer(name=args.name, prompts_dir=args.prompts_dir)
    prompt = renderer.render(data)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(prompt.text)
    else:
        print(prompt.text)
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    data = _load_data(args.data)
    renderer = Renderer(name=args.name, prompts_dir=args.prompts_dir)
    chat = renderer.chat(data)
    if args.json:
        print(json.dumps({
            'text': chat.text,
            'chat': [m.model_dump() for m in chat.chat],
        }, ensure_ascii=False, indent=2))
    else:
        for m in chat.chat:
            print(f"{m.role}: {m.content}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    if args.name:
        # resolve path based on prompts dir / name
        rel_path = args.name.replace('.', '/') + '.txt'
        path = os.path.join(args.prompts_dir, rel_path)
    else:
        path = args.path
    report = validate_template_file(path, prompts_dir=args.prompts_dir)
    if report.issues:
        for i in report.issues:
            loc = f" (line {i.line}, col {i.column})" if i.line is not None else ""
            print(f"{i.kind.upper()}: {i.message}{loc}")
    if not report.is_valid:
        return 2
    print("OK")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='promptist', description='Promptist CLI')
    sub = p.add_subparsers(dest='command', required=True)

    pr = sub.add_parser('render', help='Render a template')
    pr.add_argument('--name', required=True, help='Template name (dot notation), e.g. chat.scenario')
    pr.add_argument('--prompts-dir', required=True, help='Directory with templates')
    pr.add_argument('--data', help='JSON string or @path/to.json')
    pr.add_argument('--output', help='Write output to file')
    pr.set_defaults(func=cmd_render)

    pc = sub.add_parser('chat', help='Render as chat messages')
    pc.add_argument('--name', required=True)
    pc.add_argument('--prompts-dir', required=True)
    pc.add_argument('--data')
    pc.add_argument('--json', action='store_true', help='Print JSON output')
    pc.set_defaults(func=cmd_chat)

    pv = sub.add_parser('validate', help='Validate a template')
    g = pv.add_mutually_exclusive_group(required=True)
    g.add_argument('--name', help='Template name')
    g.add_argument('--path', help='Path to template file')
    pv.add_argument('--prompts-dir', required=True, help='Directory with templates')
    pv.set_defaults(func=cmd_validate)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())


