import re


def inspect(text, diagnostics=''):
    stripped = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', text)
    reasons = []
    if re.search(r'//|/\*', stripped):
        reasons.append('generated-comment-or-diagnostic')
    if len(text.splitlines()) > 500:
        reasons.append('physical-line-limit')
    if re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', stripped):
        reasons.append('assembly-or-blob-directive')
    if re.search(r'Warning:.*missing.*bx|[Uu]nable to decompile|[Ff]ailed to decompile|[Uu]nimplemented instruction|M2C_(?:ERROR|UNSUPPORTED)', text + '\n' + diagnostics):
        reasons.append('unsupported-decompiler-stub')
    return {'ordinarySourceCandidate': not reasons, 'physicalLines': len(text.splitlines()), 'reasons': reasons,
        'generatedDiagnosticOrStubSourceCredit': 0}


def require(text, diagnostics=''):
    result = inspect(text, diagnostics)
    if not result['ordinarySourceCandidate']:
        raise ValueError(result)
    return result
