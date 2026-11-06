import re
from project import ROOT
from parallel_status import interval
from prepare_source_cohort_v3_20261102 import classify_additions


def qualify(row, span):
    if row.get('sourceLanguage') != 'assembly':
        raise ValueError('Whole-function assembly requires explicit assembly language')
    size = span[2] - span[1]
    justification = row.get('assemblyJustification') or {}
    published = (ROOT / justification.get('publishedSource', '')).resolve()
    if not published.is_relative_to(ROOT) or not published.is_file():
        raise ValueError('Published assembly source is absent or outside the project')
    key = (row['module'], row['mode'], span[1])
    accounting = classify_additions({key: dict(row, size=size)}, {key})
    if accounting != dict(newOrdinaryCFunctions=0, newOrdinaryCBytes=0,
                          newVerifiedOriginalAssemblyFunctions=1, newVerifiedOriginalAssemblyBytes=size):
        raise ValueError('Original production assembly classification differs')
    if (row.get('ordinaryCBytes') != 0 or row.get('justifiedAssemblyBytes') != size or
            justification.get('rawExecutableBytesStoredAsSource') is not False or
            justification.get('hardwareExceptionOrCalleeExecutionCredit') != 0 or
            not justification.get('hardwareOrAbiNecessity', '').strip()):
        raise ValueError('Whole original assembly accounting or necessity differs')
    declaration = justification.get('publishedAsmDeclaration', '')
    function = justification.get('publishedFunction', '')
    original = published.read_text(encoding='utf-8')
    if (not function or not re.search(r'\basm\b[^;{}]*\b' + re.escape(function) + r'\s*\(', declaration) or
            re.sub(r'\s+', '', declaration) not in re.sub(r'\s+', '', original)):
        raise ValueError('Pinned published explicit assembly declaration is absent')
    ranges = row.get('justifiedAssemblyRanges', [])
    if len(ranges) != 1:
        raise ValueError('Whole original assembly requires one complete range')
    region = ranges[0]
    fields = {'program', 'processor', 'module', 'mode', 'address', 'offset', 'bytes'}
    if not fields.issubset(region) or region['offset'] != 0 or interval(region) != span:
        raise ValueError('Whole original assembly range differs from exact physical identity')
    return dict(address=row['address'], ordinaryCBytes=0, justifiedAssemblyBytes=size,
                publishedFunction=function, originalClassifierRetained=True)
