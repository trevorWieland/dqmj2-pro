from project import ROOT

SOURCE=ROOT/'src/runtime/parallel_wave20261106/aes-table-data'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/aes-table-data'
WORK=ROOT/'work/w6at'
REFERENCE=ROOT/'deps/reference/heimdal-a6cf94577c0d1e5bca5304342e4ddffb18255afe-rijndael'


def assert_owned():
    if SOURCE.resolve()!=(ROOT/'src/runtime/parallel_wave20261106/aes-table-data').resolve()or EVIDENCE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/aes-table-data').resolve()or WORK.resolve()!=(ROOT/'work/w6at').resolve():raise ValueError('Exact admitted AES data source/evidence/work identity differs')
    if not all(p.resolve().is_relative_to(ROOT.resolve())for p in [SOURCE,EVIDENCE,WORK,REFERENCE]):raise ValueError('AES data path escaped workspace')


def assert_work(path):
    assert_owned()
    if not path.resolve().is_relative_to(WORK.resolve()):raise ValueError('AES diagnostic/compiler output escaped owned work root')
