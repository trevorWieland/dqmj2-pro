from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

SOURCE = """typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { u16 from, to, current; } Area;
typedef struct { s32 type; Area attr, affine; u16 guid, pad; s32 fast, step; } Manager;
typedef struct { u16 words[4]; } Oam;
typedef struct { u16 reservation[128]; Oam buffer[128]; u16 affine[32]; } Cache;
typedef char CacheSize[(sizeof(Cache) == 0x540) ? 1 : -1];
typedef char ManagerFastOffset[(__offsetof(Manager, fast) == 0x14) ? 1 : -1];
extern Cache native_data_020f0f08[];
extern s32 native_data_020dcb44;
extern void native_fn_020072d0(void *, u32);
extern void native_fn_0200845c(u32, void *, u32, u32);
extern void native_fn_02008c14(u32, void *, u32);
void native_main_0203716c(Manager *manager) {
    if (manager->fast) {
        u32 size;
        Oam *data;
        if (manager->attr.current <= manager->attr.to + 1 && manager->attr.from <= manager->attr.to) {
            size = sizeof(Oam) * (u16)(manager->attr.to - manager->attr.from + 1);
        } else {
            size = 0;
        }
        data = native_data_020f0f08[manager->type].buffer + manager->attr.from;
        native_fn_020072d0(data, size);
        if (native_data_020dcb44 != -1) {
            native_fn_0200845c((u32)native_data_020dcb44, data, 192, size);
        } else {
            native_fn_02008c14(192, data, size);
        }
    } else {
        Oam *data = native_data_020f0f08[manager->type].buffer + manager->attr.from;
        const u16 count = (u16)(manager->attr.to - manager->attr.from + 1);
        u16 index;
        for (index = 0; index < count; index++) {
            data->words[0] = 192;
            data++;
        }
    }
    manager->attr.current = manager->attr.from;
    manager->affine.current = manager->affine.from;
}
"""


def main():
    reference = ROOT / 'deps/reference/NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85/libraries/g2d/src/g2d_OAM.c'
    source = ROOT / 'generated/recovery/20261101-reference-oam296/native_main_0203716c.c'
    assert not source.exists()
    source.parent.mkdir(parents=True, exist_ok=True)
    text = SOURCE.replace('__offsetof(Manager, fast)', '(u32)&((Manager *)0)->fast')
    source.write_text(text, encoding='utf-8')
    results = []
    for compiler_path in compiler.COMPILER_PINS:
        for speed in [False, True]:
            directory = ROOT / 'work/main-reference-oam296-20261101' / (compiler.COMPILER_PINS[compiler_path][:12] + '-' + str(int(speed)))
            compiler.WORK = directory / 'compile'
            rows, unused = compiler.compare(source, 'main', 2, 'off', speed=speed, compiler=ROOT / compiler_path)
            row, exact = rows[0], False
            if row.get('compileFailed'):
                proof = None
            else:
                try:
                    proof = validate(row, qualified_bindings(row), directory / 'link')
                    exact = True
                except ValueError as error:
                    assert isinstance(error.args[0], dict)
                    proof = error.args[0]
            results.append(dict(compilation=row, genuineLinkComparison=proof, exact=exact, sourceCredit=0))
            print(dict(compiler=compiler_path, speed=speed, exact=exact,
                matchingBytes=proof.get('matchingBytes', proof.get('bytes')) if proof else None), flush=True)
    write_json(ROOT / 'evidence/attempts/main-reference-oam296-20261101.json', dict(sourceCredit=0,
        generator=Path(__file__).name, generatorSha256=sha256(__file__),
        reference=reference.relative_to(ROOT).as_posix(), referenceSha256=sha256(reference),
        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), results=results,
        limitations=['Reference-assisted typed source hypothesis only',
            'Source helper names and type mappings require native/caller/interface qualification',
            'No whole SDK-version identity, source acceptance or semantic proof from isolated links']))


if __name__ == '__main__':
    main()
