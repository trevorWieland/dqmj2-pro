import re
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

MAPPING = {'NNS_G2dGetNewOamManagerInstanceAsFastTransferMode':0x02036C78,
    'NNS_G2dEntryOamManagerOam':0x02036DD4, 'NNS_G2dEntryOamManagerAffine':0x02036EA4,
    'NNS_G2dApplyOamManagerToHW':0x02036F68, 'NNS_G2dResetOamManagerBuffer':0x0203716C}


def main():
    reference = ROOT / 'deps/reference/NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85/libraries/g2d/src/g2d_OAM.c'
    text = reference.read_text(encoding='utf-8')
    replacements = [('static OamCache oamCache_[NUM_OAM_TYPES];', 'extern OamCache oamCache_[NUM_OAM_TYPES];'),
        ('static u16 numRegisterdInstance_ = 0x0;', 'extern u16 numRegisterdInstance_;')]
    for before,after in replacements:
        assert text.count(before) == 1
        text = text.replace(before,after)
    pattern = r'    static OBJLoadFunction \* funcTbl\[\] = \{.*?    \};'
    text, count = re.subn(pattern, '    extern OBJLoadFunction * native_data_020dd810[5];', text, flags=re.S)
    assert count == 1
    text = text.replace('return funcTbl[type];', 'return native_data_020dd810[type];')
    folder = ROOT / 'generated/recovery/20261101-reference-oam-family'
    folder.mkdir(parents=True, exist_ok=True)
    body = folder / 'g2d_OAM.reference.c'
    assert not body.exists()
    body.write_text(text, encoding='utf-8')
    aliases = {**{name:'native_main_' + f'{address:08x}' for name,address in MAPPING.items()},
        'DC_InvalidateRange':'native_fn_020072d0', 'DC_FlushRange':'native_fn_02007308',
        'GX_LoadOAM':'native_fn_020049fc', 'GXS_LoadOAM':'native_fn_02004a50',
        'MI_DmaFill32':'native_fn_0200845c', 'MIi_CpuClear32':'native_fn_02008c14',
        'MIi_CpuClear16':'native_fn_02008be0', 'oamCache_':'native_data_020f0f08',
        'numRegisterdInstance_':'native_data_020f0f04', 'GXi_DmaId':'native_data_020dcb44'}
    source = folder / 'source.c'
    source.write_text(''.join('#define ' + name + ' ' + alias + '\n' for name,alias in aliases.items()) +
        '#include "g2d_OAM.reference.c"\n', encoding='utf-8')
    profile = read_json(ROOT / 'evidence/attempts/main-full-reference-oam-parse-only-probe-20261101.json')
    flags = list(profile['extraFlags'])
    for index,value in enumerate(flags):
        if index and flags[index-1] == '-i':
            flags[index] = value.replace(chr(92),'/').split('/dqmj2pro-decomp/',1)[1]
    compiler.FLAGS += flags
    compiler.WORK = ROOT / 'work/main-reference-oam-family-20261101/compile'
    rows, unused = compiler.compare(source, 'main', '4,p', 'on,noauto',
        compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    assert len(rows) == len(MAPPING)
    results = []
    for row in rows:
        directory = ROOT / 'work/main-reference-oam-family-20261101/link' / row['name']
        exact = False
        try:
            proof = validate(row, qualified_bindings(row), directory)
            exact = True
        except ValueError as error:
            proof = error.args[0]
        results.append(dict(compilation=row,genuineLinkComparison=proof,exact=exact,sourceCredit=0))
        print(dict(address=row['address'], bytes=row['bytes'], exact=exact,
            proof=str(proof)[:180] if not exact else 'Full real-link span exact'), flush=True)
    write_json(ROOT / 'evidence/attempts/main-reference-oam-family-20261101.json', dict(sourceCredit=0,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),
        reference=reference.relative_to(ROOT).as_posix(),referenceSha256=sha256(reference),
        source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),
        body=body.relative_to(ROOT).as_posix(),bodySha256=sha256(body),
        explicitBindingOnlyDeclarationChanges=replacements,originalStaticDataSourceCredit=0,
        functionTableBinding='main020DD810 five pointer words, native Apply literal02037168',
        inferredFunctionNames=MAPPING,results=results,parseOnlyHeadersNotAdopted=True,
        limitations=['Reference-assisted source hypotheses only; source/type/caller/native/module qualification pending',
            'SDK version alignment is not established by these separate function comparisons',
            'Known original data remain external scaffolding, never recovered executable bytes',
            'The reset raw signed-word return alternative is separate; these SDK formal views are not admitted']))


if __name__ == '__main__':
    main()
