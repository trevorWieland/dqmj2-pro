import re
from project import ROOT, configuration


def return_catalogue(module):
    from ledger_state import collect_matches
    accepted, unused = collect_matches(configuration()['romSha256'])
    sources, symbols, result = {}, {}, {}
    for item in accepted.values():
        scope = item['module']
        if scope not in {'main', module} or not item['source'].lower().endswith(('.c', '.cpp')):
            continue
        path = ROOT / item['source']
        if path not in sources:
            sources[path] = path.read_text(encoding='utf-8-sig')
        name = re.escape(item['name'])
        signature = re.search(r'^\s*(?:static\s+)?((?:const\s+)?(?:void|u8|s8|u16|s16|u32|s32|u64|s64|f32|f64|int|unsigned int|float|double)(?:\s*\*)?)\s*' + name + r'\s*\([^;{}]*\)\s*\{', sources[path], re.M)
        if not signature:
            continue
        return_type = signature[1].strip()
        if '*' in return_type:
            return_type = 'u8 *'
        return_type = {'unsigned int': 'u32', 'int': 's32', 'float': 'f32', 'double': 'f64'}.get(return_type, return_type)
        if return_type == 'u32':
            continue
        if scope not in symbols:
            config = ROOT / ('config/arm9/symbols.txt' if scope == 'main' else f'config/arm9/overlays/{scope}/symbols.txt')
            symbols[scope] = {(mode, int(address, 16)): alias for alias, mode, address in re.findall(r'^(\S+) kind:function\((arm|thumb),[^\n]*\) addr:0x([0-9a-f]+)', config.read_text(), re.M)}
        alias = symbols[scope].get((item['mode'], item['address']))
        if not alias or not alias.startswith('func_'):
            continue
        result[alias] = {'type': return_type, 'module': scope, 'address': hex(item['address']), 'mode': item['mode'], 'source': item['source'], 'sourceSha256': item['sourceSha256']}
    return result


def apply_context(context, catalogue):
    def replace(match):
        name = match[1]
        return 'extern ' + catalogue[name]['type'] + ' ' + name + '();' if name in catalogue else match[0]
    return re.sub(r'extern u32 (func_\w+)\(\);', replace, context)
