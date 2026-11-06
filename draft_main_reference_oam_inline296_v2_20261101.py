from pathlib import Path
import match_runtime as compiler
from project import ROOT, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from draft_main_reference_oam296_20261101 import SOURCE

HELPERS = """static inline s32 valid(Area *area) {
    return (s32)((area->current <= area->to + 1) && (area->from <= area->to));
}
static inline Cache *cache(s32 type) { return &native_data_020f0f08[type]; }
static inline Oam *buffer(s32 type, u16 index) {
    Cache *value = cache(type);
    return value->buffer + index;
}
static inline Oam *from(Manager *manager) {
    Oam *value = buffer(manager->type, manager->attr.from);
    return value;
}
static inline u32 size(Area *area) {
    if (valid(area)) {
        return (u32)(sizeof(Oam) * (u16)(area->to - area->from + 1));
    } else { return 0; }
}
static inline void fill(u32 dma, void *dest, u32 value, u32 length) {
    if (dma != 0xFFFFFFFFU) { native_fn_0200845c(dma, dest, value, length); }
    else { native_fn_02008c14(value, dest, length); }
}
static inline void reset(s32 type, u16 first, u16 last) {
    Oam *data = buffer(type, first);
    const u16 count = (u16)(last - first + 1);
    u16 index;
    for (index = 0; index < count; index++) {
        *((u16 *)data) = 192;
        data++;
    }
}
void native_main_0203716c(Manager *manager) {
    if (manager->fast) {
        const u32 length = size(&manager->attr);
        void *data = from(manager);
        native_fn_020072d0(data, length);
        fill((u32)native_data_020dcb44, data, 192, length);
    } else {
        reset(manager->type, manager->attr.from, manager->attr.to);
    }
    manager->attr.current = manager->attr.from;
    manager->affine.current = manager->affine.from;
}
"""


def main():
    source = ROOT / 'generated/recovery/20261101-reference-oam-inline296/native_main_0203716c.c'
    assert source.is_file()
    source.parent.mkdir(parents=True, exist_ok=True)
    head = SOURCE.split('void native_main_0203716c')[0]
    head = head.replace('__offsetof(Manager, fast)', '(u32)&((Manager *)0)->fast')
    assert source.read_text(encoding='utf-8') == head + HELPERS
    compiler.FLAGS += ['-lang', 'c99', '-ipa', 'file']
    results = []
    for compiler_path in list(compiler.COMPILER_PINS)[1:]:
        for optimization in [2, '4,p']:
            for inline in ['on,noauto', 'auto']:
                directory = ROOT / 'work/main-reference-oam-inline296-v2-20261101' / compiler.COMPILER_PINS[compiler_path][:12] / (str(optimization) + '-' + inline).replace(',', '-')
                compiler.WORK = directory / 'compile'
                rows, unused = compiler.compare(source, 'main', optimization, inline, compiler=ROOT / compiler_path)
                row, exact = rows[0], False
                if row.get('compileFailed'): proof = None
                else:
                    try:
                        proof = validate(row, qualified_bindings(row), directory / 'link')
                        exact = True
                    except ValueError as error:
                        assert isinstance(error.args[0], dict)
                        proof = error.args[0]
                results.append(dict(compilation=row, genuineLinkComparison=proof, exact=exact, sourceCredit=0))
                print(dict(compiler=compiler_path, optimization=optimization, inline=inline, exact=exact,
                    matchingBytes=proof.get('matchingBytes', proof.get('bytes')) if proof else None), flush=True)
    write_json(ROOT / 'evidence/attempts/main-reference-oam-inline296-v2-20261101.json', dict(sourceCredit=0,
        generator=Path(__file__).name, generatorSha256=sha256(__file__),
        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), results=results,
        limitations=['Reference-assisted source hypothesis with compatible helper views; historical type/caller and native fixtures unproved']))


if __name__ == '__main__':
    main()
