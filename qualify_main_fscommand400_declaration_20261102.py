from project import ROOT, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    original = ROOT / 'nonmatching/main/20261102-nitrosdk-closed-breadth/native_main_0200a63c.c'
    text = original.read_text(encoding='utf-8')
    declaration = 'extern FSResult (*const native_data_main_020d8c28[])(FSFile *);\n'
    marker = 'FSResult native_main_0200a63c(FSFile * p_file, FSCommandType command);'
    assert text.count(marker) == 1
    text = text.replace(marker, declaration + marker)
    source = ROOT / 'nonmatching/main/20261102-fscommand400-typed-table/native_main_0200a63c.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding='utf-8')
    builder.WORK = ROOT / 'work/main-fscommand400-typed-table-20261102'
    row, proof, body = builder.build(source, 'positive', True)
    write_json(ROOT / 'evidence/attempts/main-fscommand400-typed-table-20261102.json',
        dict(sourceCredit=0, genuineExact=True, linkedBytes=len(body), compiledEntry=row, genuineLinkProof=proof,
            source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            originalMissingDeclarationSource=original.relative_to(ROOT).as_posix(), originalSourceSha256=sha256(original),
            restoredOriginalPreprocessedDeclaration='extern FSResult (*const (fsi_default_command[]))(FSFile *);',
            originalStorageSourceCredit=0, actualNativeReturns=0))
    print(dict(genuineExact=True, bytes=len(body), originalStorageSourceCredit=0, sourceCredit=0))


if __name__ == '__main__':
    main()
