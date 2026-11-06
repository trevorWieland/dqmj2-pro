from project import ROOT,sha256

PINS={'src/runtime/grid12/grid12.c': 'af8238a5f3d050637b076161683b7d5e65c14ed31221d699843e5e7e729c26eb', 'src/save_recovery_records.c': 'cb6891e60297df0b4df002ff9ef04e28e70c19fe7d1964d7845f8fcc04571b14', 'src/runtime/runtime05/native_main_020629e0.c': '2b8cdcf9c44f6f55207338fe94dc0e09f6f49672d0a2d603c3da3991fb8453e3', 'src/runtime/parallel_wave20261105/main-tail-next/fifth/020d0a24.c': '7f3bf897771cb3debc0d2fe3a070cdcdfdffe45d688b138843792bb73df28be5', 'src/runtime/runtime09/native_main_020d0218.c': '1da2971dbaf727e0c4e3b98493cf503184e726d14d816118b2e5419995b820e9', 'src/runtime/runtime09/native_main_020d0210.c': '5fc3493e3e987a2c9dc291adb9d616c900b65d4cce32deecbd2bd6d83128894b', 'src/runtime/runtime09/native_main_020d0208.c': '55a43961cd13a934dcc5868fc9219bf859151d8c082638fb4ed1a976e08e2d46'}

def qualify():
    for name,digest in PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError("Existing measured game source lineage changed")
    return dict(origin="Original native ARM instructions and existing measured ordinary C; no scene semantics inferred",pins=[dict(path=name,sha256=digest)for name,digest in PINS.items()],helperCodeAndStorageCredit=0,unusedDeclarationsDoNotProveProviderABI=True)
