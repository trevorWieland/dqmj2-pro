import gzip
import json
import gc
from project import ROOT, sha256, write_json
import match_ov000_birth395_20261031 as P
from save_link_snapshots import freeze_link
SOURCE = ROOT / 'src/overlays/ov000_20261101_latch786/source.c'
WORK = ROOT / 'work/ol786'

def main():
    old = ROOT / 'src/overlays/ov000_20261031_birth395'
    header = (old / 'context.h').read_text()
    expected = header.replace('u32 native_fn_02062358(s8)', 'u32 native_fn_02062358(u32)')
    if SOURCE.read_bytes() != (old / 'source.c').read_bytes() or SOURCE.with_name('context.h').read_text() != expected:
        raise ValueError('786 source/declaration-only provenance differs')
    if SOURCE.read_text().count('native_fn_02062358(1)') != 1:
        raise ValueError('786 unique constant1 setter site differs')
    pins = json.loads(P.PINS.read_text())
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError('786 frozen395 dependency differs')
    P.WORK = WORK
    arm, save, assets = P.F.inputs()
    meta, overlay, _ = P.measured_module('ov000')
    row, proof, body = P.compile_unit(SOURCE, 'caller', True)
    pairs = []
    observed = set()
    for index, profile in enumerate(P.G.profiles(save)):
        original = P.execute(arm, save, assets, overlay, profile)
        candidate = P.execute(arm, save, assets, overlay, profile, body)
        if original != candidate:
            raise ValueError(('786 full original/candidate behavior differs', profile))
        original.pop('_ram')
        observed.update(original['observedCodeBytes'])
        raw = P.encoded(original)
        compressed = gzip.compress(raw, mtime=0)
        path = ROOT / 'evidence/generated/latch786' / (P.c.sha(compressed) + '.json.gz')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(compressed)
        pairs.append(dict(profile=profile, actualReturns=2, nativeDependencyActualReturns=2 * original['nativeDependencyActualReturns'], providedCalls=2 * original['providedCalls'], preparationActualReturns=2 * original['preparation']['actualReturns'], preparationNativeDependencyActualReturns=2 * original['preparation']['nativeDependencyActualReturns'], preparationProvidedCalls=2 * original['preparation']['providedCalls'], trace=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)), model=original['model']))
        del original, candidate
        gc.collect()
        if index % 100 == 0:
            print('786 pairs', index + 1, flush=True)
    report = dict(schemaVersion=1, sourceCredit=0, candidateNewFunctions=0, candidateNewBytes=0, existingAlternativeBytes=1460, processor='arm9', program='', module='ov000', moduleSha256=meta['sha256'], address='0x0221b070', mode='arm', candidate=row, genuineLinkComparison=freeze_link(proof), originalSourceSha256=sha256(old / 'source.c'), originalHeaderSha256=sha256(old / 'context.h'), newHeaderSha256=sha256(SOURCE.with_name('context.h')), pairs=len(pairs), actualReturns=2 * len(pairs), nativeDependencyActualReturns=sum((p['nativeDependencyActualReturns'] for p in pairs)), providedCalls=sum((p['providedCalls'] for p in pairs)), observedOwnCodeBytes=len(observed), preparationActualReturns=sum((p['preparationActualReturns'] for p in pairs)), results=pairs, generatorSha256=sha256(__file__), limits=['Only the constant1 call has a new declaration; existing395 source and every earlier proof remain unchanged.', 'The frozen395 corpus includes explicit supplied setter/UI/file/audio boundaries; it supplies no new native setter execution.', 'Fullword setter and main396 behavior are separately pinned by Save312 for joint adoption.', 'Source body bytes and entire1460-byte linked native extent are unchanged; zero new coverage and no source-preference edits.'])
    write_json(ROOT / 'evidence/matches/ov000-20261101-latch786-zero-credit.json', report)
    print({k: report[k] for k in ['actualReturns', 'nativeDependencyActualReturns', 'providedCalls', 'observedOwnCodeBytes']})
if __name__ == '__main__':
    main()
