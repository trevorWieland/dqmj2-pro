import re
from project import ROOT, sha256
from wave20261105_weak_source_scope_proof import inspect, reloc_shape


def prove(item, row, directory):
    name = row['name']
    compiler, raw = inspect(ROOT / row['object'], name)
    split, split_raw = inspect(directory / 'caller.o', name)
    linked, linked_raw = inspect(directory / 'linked.elf', name, directory / 'caller.bin', int(row['address'], 0))
    assert compiler['binding'] == split['binding'] == linked['binding'] == 14
    assert compiler['type'] == split['type'] == linked['type'] == 2
    assert compiler['bytes'] == split['bytes'] == linked['bytes'] == 2300
    assert raw == split_raw and reloc_shape(compiler) == reloc_shape(split)
    source = ROOT / item['source']
    published = ROOT / item['provenance']['referenceSource']
    assert sha256(source) == item['sourceSha256'] and sha256(published) == item['provenance']['referenceSourceSha256']
    declaration = 'SDK_WEAK_SYMBOL int STD_TVSNPrintf (char * dst, size_t len, const char * fmt, va_list vlist)'
    assert declaration in re.sub(r'\s+', ' ', published.read_text())
    assert '__declspec(weak) int native_main_0201a670 ' in re.sub(r'\s+', ' ', source.read_text())
    assert linked_raw == (ROOT / 'extract/arm9/arm9.bin').read_bytes()[0x1a670:0x1a670 + 2300]
    export = dict(name=name, address=row['address'], bytes=2300, source=item['source'], sourceSha256=item['sourceSha256'],
        publishedSource=item['provenance']['referenceSource'], publishedSourceSha256=item['provenance']['referenceSourceSha256'], publishedWeakDeclaration=declaration)
    return dict(export=export, compiler=compiler, split=split, finalElf=linked, fullNativeInitializedBytesExact=True,
        originalObjectRelocationsAndEncodedWordsPreserved=True, originalAliasesAndStrongScopesUnchanged=True,
        sourceByteCredit=0, limits='Preserves only the defined canonical source-export scope justified by this actual binding14 and published weak declaration; global coordinator symbol checks remain required.')
