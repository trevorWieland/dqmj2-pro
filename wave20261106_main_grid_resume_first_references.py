from project import ROOT,sha256


PINS={'src/runtime/20261102_group_grid292/native_main_020d0ad8.c':'7a1d7a0b00497286be36a3d0be0ed02287136e3b81c9d3192da9e9a29e6b1029','src/save_recovery_records.c':'cb6891e60297df0b4df002ff9ef04e28e70c19fe7d1964d7845f8fcc04571b14','src/runtime/grid12/grid12.c':'af8238a5f3d050637b076161683b7d5e65c14ed31221d699843e5e7e729c26eb','main_group_grid292_fixture_v2_20261102.py':'c01471ec8c9899b79217b0e43974a04c053ea1bf063e40f53cce09786a5024a7'}


def qualify():
    for name,digest in PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError('Actual original grid source/model lineage changed')
    records=(ROOT/'src/save_recovery_records.c').read_text(encoding='utf-8')
    if 'u8 prefix[0x14]; u32 id; u8 remaining[0x6c];'not in records or 'while (index < 100)'not in records:raise ValueError('Existing132-byte saved-record view lineage differs')
    return dict(origin='Existing measured ordinary C and native execution model; no public revision or scene semantics inferred',pins=[dict(path=name,sha256=digest)for name,digest in PINS.items()],helperCodeAndStorageCredit=0,unmodifiedOldSourceAndModel=True)
