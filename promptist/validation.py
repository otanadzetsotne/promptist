import os
from dataclasses import dataclass
from typing import List, Optional, Set

from promptist.constants import RGX_PLACEHOLDER, SUPPORTED_PLACEHOLDER_TYPES


@dataclass
class ValidationIssue:
    kind: str
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    placeholder: Optional[str] = None


@dataclass
class ValidationReport:
    is_valid: bool
    issues: List[ValidationIssue]

    def raise_for_errors(self):
        errors = [i for i in self.issues if i.kind == 'error']
        if errors:
            msgs = [f"{e.kind}: {e.message} (line={e.line}, col={e.column})" for e in errors]
            raise ValueError("\n".join(msgs))


def _collect_placeholders(text: str):
    for match in RGX_PLACEHOLDER.finditer(text):
        yield match


def validate_template_text(text: str, *, prompts_dir: Optional[str] = None) -> ValidationReport:
    issues: List[ValidationIssue] = []

    # Placeholder validation
    for match in _collect_placeholders(text):
        ph_type = match.group('type')
        ph_name = match.group('name')
        ph_full = match.group('placeholder')
        start = match.start()
        line = text.count('\n', 0, start) + 1
        col = start - (text.rfind('\n', 0, start) + 1)

        if ph_type not in SUPPORTED_PLACEHOLDER_TYPES:
            issues.append(ValidationIssue(
                kind='error',
                message=f"Unsupported placeholder type: '{ph_type}' in {ph_full}",
                line=line,
                column=col,
                placeholder=ph_full,
            ))
        if ph_type == 'include':
            if prompts_dir:
                rel_path = ph_name.replace('.', '/') + '.txt'
                full_path = os.path.join(prompts_dir, rel_path)
                if not os.path.exists(full_path):
                    issues.append(ValidationIssue(
                        kind='error',
                        message=f"Included template not found: {rel_path}",
                        line=line,
                        column=col,
                        placeholder=ph_full,
                    ))

    # Role lines basic validation
    roles: Set[str] = {"system", "user", "assistant"}
    for idx, line_text in enumerate(text.split('\n'), start=1):
        ls = line_text.strip()
        if not ls:
            continue
        if ':' in ls:
            role_candidate = ls.split(':', 1)[0].lower()
            if role_candidate and role_candidate[-1] == ':':
                role_candidate = role_candidate[:-1]
            if role_candidate in {"system", "user", "assistant", "tool"}:  # allow 'tool' future-proof
                continue
            # Looks like a role line but role unknown
            if ls.endswith(':'):
                issues.append(ValidationIssue(
                    kind='warning',
                    message=f"Unknown role prefix: '{role_candidate}:'",
                    line=idx,
                    column=0,
                ))

    return ValidationReport(is_valid=not any(i.kind == 'error' for i in issues), issues=issues)


def validate_template_file(path: str, *, prompts_dir: Optional[str] = None) -> ValidationReport:
    if not os.path.exists(path):
        return ValidationReport(is_valid=False, issues=[ValidationIssue(kind='error', message=f"Template file not found: {path}")])
    with open(path, 'r') as f:
        text = f.read()
    # If prompts_dir not provided, infer from path
    if prompts_dir is None:
        prompts_dir = os.path.dirname(path)
    return validate_template_text(text, prompts_dir=prompts_dir)


