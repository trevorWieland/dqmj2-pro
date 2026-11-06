from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from replay_main_slot_register_attempts_20261031 import attempt


def main():
    frozen = read_json(ROOT / 'evidence/attempts/main-slot-register-consolidated-20261031.json')
    inputs = {}
    for name in ['order-06', 'order-09', 'cached-u8']:
        path = ROOT / f'nonmatching/main-runtime/20261031-slot-register/{name}/native_main_02015c70.c'
        row = next(row for row in frozen['matches'] if row['source'] == path.relative_to(ROOT).as_posix())
        assert sha256(path) == row['sourceSha256']
        inputs[name] = path
    reused = []
    base = inputs['order-09'].read_text(encoding='utf-8')
    old = '        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, 0x1D54) = (s32) (arg1 + 0x1E8);\n        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, 0x1D58) = (s32) (arg1 + 0x258);'
    for first in ['arg0', 'first_record']:
        for second in ['var_r4', 'arg1', 'second_record']:
            text = base.replace('    u8 var_r4;', '    u32 var_r4;\n    u32 first_record;\n    u32 second_record;')
            new = f'        {first} = arg1 + 0x1E8;\n        {second} = arg1 + 0x258;\n        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, 0x1D54) = (s32) {first};\n        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, 0x1D58) = (s32) {second};'
            assert old in text
            reused.extend(attempt('reused-' + first + '-' + second, text.replace(old, new)))
    profiles = []
    for profile in ['1', '2,p', '2,s', '3', '3,p', '3,s', '4', '4,p', '4,s']:
        compiler.WORK = ROOT / ('work/main-slot-register-20261031/profile-' + profile.replace(',', '-'))
        rows, unused = compiler.compare(inputs['order-06'], 'main', profile, 'off', True)
        profiles.extend(rows)
    identities, conversions = [], []
    for executable in compiler.COMPILER_PINS:
        for name, source in inputs.items():
            label = executable.replace('/', '-')
            compiler.WORK = ROOT / f'work/main-slot-register-20261031/compiler-{label}/{name}'
            rows, unused = compiler.compare(source, 'main', 2, 'off', True, compiler=ROOT / executable)
            identities.extend(rows)
    for name, source in inputs.items():
        base = source.read_text(encoding='utf-8')
        for kind in ['void', 'u8', 'global-pointer']:
            if kind == 'global-pointer':
                text = base.replace('extern u32 native_data_020ec36c;', 'extern u8 *native_data_020ec36c;')
            else:
                text = base.replace('temp_r9 = native_data_020ec36c + 0x1788 + temp_r6;',
                                    f'temp_r9 = ({kind} *)(native_data_020ec36c + 0x1788 + temp_r6);')
            if kind == 'u8':
                text = text.replace('void *temp_r9;', 'u8 *temp_r9;')
            path = ROOT / f'nonmatching/main-runtime/20261031-slot-legacy-compiler/{name}-{kind}/source.c'
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.read_bytes() != text.encode():
                raise ValueError('Earlier explicit pointer-conversion source differs')
            path.write_bytes(text.encode())
            compiler.WORK = ROOT / f'work/main-slot-legacy-compiler-20261031/{name}-{kind}'
            rows, unused = compiler.compare(path, 'main', 2, 'off', True,
                                            compiler=ROOT / 'tools/mwccarm/mwccarm/1.2/base/mwccarm.exe')
            conversions.extend(rows)
    reports = {'reused-values': reused, 'compiler-profiles': profiles,
               'compiler-identities': identities, 'explicit-pointer-conversions': conversions}
    for suffix, rows in reports.items():
        write_json(ROOT / f'evidence/attempts/main-slot-register-{suffix}-20261031.json',
                   dict(matches=rows, sourceCredit=0, registered=False))
    print(dict(reused=len(reused), profiles=len(profiles), identities=len(identities),
               conversions=len(conversions), sourceCredit=0))


if __name__ == '__main__':
    main()
