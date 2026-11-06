import argparse
import ast
from project import ROOT, read_json, write_json, sha256
from static_json_reads_20261031 import required_json_reads


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    parser.add_argument('--closure', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    config = read_json(ROOT / args.configuration)
    spec = read_json(ROOT / (config['name'] + '-specification.json'))
    ready_pins = {r['path']: r['sha256'] for r in spec['readyPacketInputs']}
    closure = read_json(ROOT / args.closure)
    files = {p for p in closure['sourceAndEvidenceHashes'] if p.endswith('.py')}
    packet_pins = []
    for name in config['readyPackets']:
        assert sha256(ROOT / name) == ready_pins[name]
        ready = read_json(ROOT / name)
        pins = ready.get('files', [])
        if 'sourceManifest' in ready:
            assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
            pins = read_json(ROOT / ready['sourceManifest'])['files']
        for pin in pins:
            path = pin['path']
            if path.endswith('.py') and path.split('/')[0] not in {'deps', 'tools', 'inputs', 'work', 'build', 'extract'}:
                assert sha256(ROOT / path) == pin['sha256']
                files.add(path)
                packet_pins.append(pin)
    inputs, reads = {}, {}
    for name in sorted(files):
        assert (ROOT / name).is_file()
        inputs[name] = sha256(ROOT / name)
        tree = ast.parse((ROOT / name).read_text(encoding='utf-8-sig'))
        for path in required_json_reads(tree, ROOT):
            if path.split('/')[0] not in {'deps', 'tools', 'inputs', 'work', 'build', 'extract'}:
                reads.setdefault(path, []).append(name)
    missing = [dict(path=p, staticReaders=names) for p, names in sorted(reads.items()) if not (ROOT / p).is_file()]
    assert all(sha256(ROOT / p) == h for p, h in inputs.items())
    write_json(ROOT / args.output, dict(passed=True, sourceCredit=0, advisoryOnly=True,
        configuration=args.configuration, configurationSha256=sha256(ROOT / args.configuration),
        previousClosure=args.closure, previousClosureSha256=sha256(ROOT / args.closure),
        codeInputs=[dict(path=p, sha256=h) for p, h in sorted(inputs.items())],
        frozenPacketCodePinsVerified=len(packet_pins), requiredJsonPaths=len(reads),
        currentlyMissingStaticReads=missing, originalCollectorAndChecksUnchanged=True,
        generatorSha256=sha256(__file__), limitations=[
            'Advisory static reads from prior captured code and pending packet code only.',
            'Branch-insensitive reads include retired actions and future generated reports.',
            'No read is waived, no missing artifact is fabricated and no source credit is granted.',
            'The complete original capture and committed audits remain mandatory.']))
    print(dict(cohort=config['cohort'], codeFiles=len(inputs), staticJsonPaths=len(reads),
               currentlyMissing=len(missing), advisoryOnly=True))


if __name__ == '__main__':
    main()
