import argparse
import json
from pathlib import Path, PurePosixPath


MEASURES = {
    'fuzzy_match_percent', 'total_code', 'matched_code', 'matched_code_percent',
    'total_data', 'matched_data', 'matched_data_percent', 'total_functions',
    'matched_functions', 'matched_functions_percent', 'complete_code',
    'complete_code_percent', 'complete_data', 'complete_data_percent',
    'total_units', 'complete_units',
}
UNIT_METADATA = {'complete', 'module_name', 'module_id', 'source_path', 'progress_categories', 'auto_generated'}


def fields(value, allowed, label):
    if not isinstance(value, dict) or set(value) - allowed:
        raise ValueError('Unsupported public report fields: ' + label)


def number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError('Report measure must be numeric')
    result = float(value)
    if not 0 <= result < float('inf'):
        raise ValueError('Report measure is negative or nonfinite')
    return result


def measures(value):
    fields(value, MEASURES, 'measures')
    for key, entry in value.items():
        result = number(entry)
        if key.endswith('_percent') and result > 100:
            raise ValueError('Report percentage exceeds 100')


def source_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Source path must be repository relative')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or path.parts[0] not in {'src', 'include', 'generated'}:
        raise ValueError('Source path leaves public source directories')


def validate(report, project, denominator):
    fields(report, {'version', 'measures', 'units', 'categories'}, 'report')
    if report.get('version') != 2:
        raise ValueError('Expected pinned objdiff report version 2')
    measures(report.get('measures'))
    totals = report['measures']
    if int(totals.get('total_code', 0)) + int(totals.get('total_data', 0)) != denominator:
        raise ValueError('Report does not cover the complete initialized-byte denominator')
    expected = {unit['name']: unit for unit in project['units']}
    if len(expected) != len(project['units']):
        raise ValueError('Duplicate project unit name')
    actual = report.get('units')
    if not isinstance(actual, list) or len(actual) != len(expected):
        raise ValueError('Report unit count differs from project')
    seen = set()
    for unit in actual:
        fields(unit, {'name', 'measures', 'sections', 'functions', 'metadata'}, 'unit')
        name = unit.get('name')
        if name not in expected or name in seen:
            raise ValueError('Unexpected or duplicate report unit')
        seen.add(name)
        measures(unit.get('measures', {}))
        metadata = unit.get('metadata', {})
        fields(metadata, UNIT_METADATA, 'unit metadata')
        source_path(metadata.get('source_path'))
        configured = expected[name]['metadata']
        if metadata.get('source_path') != configured['source_path'] or bool(metadata.get('complete')) != bool(configured.get('complete')):
            raise ValueError('Report source or completion differs from checked project')
        for group in ('sections', 'functions'):
            for item in unit.get(group, []):
                fields(item, {'name', 'size', 'fuzzy_match_percent', 'metadata', 'address'}, group)
                if not isinstance(item.get('name'), str):
                    raise ValueError('Report item needs a symbol or section name')
                number(item.get('size', 0))
                if 'address' in item:
                    number(item['address'])
                if 'fuzzy_match_percent' in item and number(item['fuzzy_match_percent']) > 100:
                    raise ValueError('Item percentage exceeds 100')
                fields(item.get('metadata', {}), {'demangled_name', 'virtual_address'}, 'item metadata')
    for category in report.get('categories', []):
        fields(category, {'id', 'name', 'measures'}, 'category')
        measures(category.get('measures', {}))
    return {'validatedUnits': len(seen), 'initializedBytes': denominator, 'publicSchemaPassed': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--denominator', type=int, default=2512636)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding='utf-8'))
    project = json.loads(args.project.read_text(encoding='utf-8'))
    result = validate(report, project, args.denominator)
    export_path = args.project.parent / 'export-receipt.json'
    if export_path.is_file():
        exported = json.loads(export_path.read_text(encoding='utf-8'))
        if exported.get('publishable') is True:
            expected = {'matched_code': exported['acceptedFunctionCodeBytes'], 'complete_code': exported['acceptedFunctionCodeBytes'],
                        'matched_data': exported['matchedTypedDataBytes'], 'complete_data': exported['matchedTypedDataBytes']}
            if any(int(report['measures'].get(key, 0)) != value for key, value in expected.items()):
                raise ValueError('objdiff matching counts differ from verified source compilation and linkage')
            result['matchedCodeBytes'] = expected['matched_code']
            result['matchedDataBytes'] = expected['matched_data']
    print(json.dumps(result))


if __name__ == '__main__':
    main()
