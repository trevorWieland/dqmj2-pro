import copy
from project import ROOT, read_json, sha256
from source_packet_audit import identity, snapshot_link
from source_dependencies import dependencies_current

CONTRACT_FIELDS = ('bytes','source','sourceSha256','targetSha256','compiler','compilerSha256','compilerFlags')

def local(name, existing=True):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or existing and not path.is_file():
        raise ValueError('Missing or escaping source packet path: ' + name)
    return path

def pin(path, expected):
    if sha256(local(path)) != expected:
        raise ValueError('Pinned source packet input differs: ' + path)

def producer_command(command, interpreter):
    from pathlib import Path
    result = list(command)
    if result and Path(result[0]).name.lower() in ('python.exe','python3.exe','python','python3'):
        if Path(result[0]).resolve() != Path(interpreter).resolve():
            raise ValueError('Historical launcher is not the current trusted Python interpreter')
        result.pop(0)
    if not result or local(result[0]).suffix != '.py' or not local(result[0]).is_file():
        raise ValueError('Source packet requires a repository-local Python producer')
    return result

def recipe_aliases(row):
    row = copy.deepcopy(row)
    for canonical, original in (('compiler','compilerPath'),('compilerFlags','flags')):
        if canonical in row and original in row and row[canonical] != row[original]:
            raise ValueError('Conflicting original compiler recipe aliases: ' + canonical)
        if canonical not in row and original in row:
            row[canonical] = copy.deepcopy(row[original])
    if not isinstance(row.get('compiler'),str) or not isinstance(row.get('compilerFlags'),list) or not row['compilerFlags']:
        raise ValueError('Explicit original compiler path and flags required')
    return row

def checked_row(row, report):
    row = recipe_aliases(row)
    if not isinstance(row['bytes'],int) or isinstance(row['bytes'],bool) or row['bytes'] <= 0 or row['compiledBytes'] != row['bytes']:
        raise ValueError('Complete positive source extent required')
    for name in ('source','object','compiler'):
        pin(row[name], row[name + 'Sha256'])
    if not dependencies_current(row, report):
        raise ValueError('Incomplete or stale source include closure')
    is_data = row.get('kind') == 'data'
    route = 'standard-matching-schema'
    if not row.get('exactAfterDeclaredRelocation'):
        if is_data:
            raise ValueError('Data requires its explicit byte/placement proof')
        route = snapshot_link(row, pin)
        row['realLink'] = read_json(local(row['realLinkSnapshot']['isolatedCallerLinkValidation']))
        row['exactAfterDeclaredRelocation'] = True
        row['canonicalNativeSnapshotAdapter'] = dict(sourceObjectUnchanged=True, bytesOrSymbolsRenamed=False,
            originalSchema='exactByteEqual/genuineMWLinked/realLinkSnapshot', sourceOrByteCredit=0)
    link = row.get('realLink', {})
    if not (link.get('exactDataBytes') and link.get('exactDataAddress') if is_data else link.get('exactCallerBytes')):
        raise ValueError('Complete genuine native link required')
    return row, route

def validate_rows(report, expected):
    if report.get('allPassed') is not True or report.get('failed'):
        raise ValueError('Source packet did not pass its original gates')
    rows = report.get('matches',[]) + report.get('dataMatches',[])
    wanted = {identity(row):recipe_aliases(row) for row in expected}
    actual = {identity(row):row for row in rows}
    if len(wanted) != len(expected) or len(actual) != len(rows) or set(actual) != set(wanted):
        raise ValueError('Source packet identity set differs')
    output, routes = [], []
    for row in rows:
        row = recipe_aliases(row)
        for field in CONTRACT_FIELDS:
            if row.get(field) != wanted[identity(row)].get(field):
                raise ValueError('Frozen source/native/compiler contract differs: ' + field)
        checked, route = checked_row(row, report)
        output.append(checked)
        routes.append(route)
    return output, routes
