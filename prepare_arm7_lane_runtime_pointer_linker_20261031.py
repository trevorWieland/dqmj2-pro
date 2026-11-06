from project import ROOT,sha256


def main():
    base=ROOT/'link_arm7_bulk_20261030.py'
    base_sha='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
    if sha256(base)!=base_sha:
        raise ValueError('Frozen standard linker source differs')
    proof='evidence/attempts/arm7-lane-setting-producer-20261031.json'
    proof_sha='e372dd000041574275ca9852f7f5ca57a4fbe41acb4a1c0c4eed50ad8447c8f4'
    if sha256(ROOT/proof)!=proof_sha:
        raise ValueError('Frozen original producer qualification differs')
    text=base.read_text()
    old="    else:\n        raise ValueError('Unqualified external ARM7 data target: ' + hex(target))\n"
    new=f'''    elif target == 0x0380FFF4:
        expected_identity = ('', 'arm7', 'arm7-main', 'arm', '0x27e8ec8', 52)
        actual_identity = tuple(entry.get(key, '') for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes'))
        qualification = {{'report': '{proof}', 'sha256': '{proof_sha}', 'storageBytes': 4}}
        if actual_identity != expected_identity or entry.get('runtimePointerQualification') != qualification:
            raise ValueError('External runtime pointer lacks its exact qualified caller/word contract')
        evidence = ROOT / qualification['report']
        if digest(evidence.read_bytes()) != qualification['sha256'] or digest((ROOT / 'link_arm7_bulk_20261030.py').read_bytes()) != '{base_sha}':
            raise ValueError('External runtime pointer producer/base policy differs')
        report = json.loads(evidence.read_text())
        if digest((ROOT / report['generator']).read_bytes()) != report['generatorSha256']:
            raise ValueError('External runtime pointer producer generator differs')
        if report['storage'] != '0x0380fff4' or report['storageBytes'] != 4 or report['origin'] != 'incoming descriptor word0' or report['constructorReturnCredit'] != 0 or report['moduleBssOwnership'] is not False:
            raise ValueError('External runtime pointer producer scope differs')
        return {{'program': '', 'processor': 'arm7', 'module': 'external-arm7-runtime-pointer-word',
            'kind': 'data', 'mode': 'data', 'address': hex(target), 'region': 'descriptor-produced-absolute-pointer-no-module-ownership',
            'storageBytes': 4, 'producerQualification': qualification, 'sourceCredit': 0}}
    else:
        raise ValueError('Unqualified external ARM7 data target: ' + hex(target))
'''
    if text.count(old)!=1:
        raise ValueError('Expected unique standard linker refusal guard absent')
    text=text.replace(old,new)
    destination=ROOT/'link_arm7_runtime_pointer_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace different qualified runtime pointer policy')
    destination.write_text(text)
    print(dict(linkerPolicySha256=sha256(destination),baseSha256=base_sha,storageBytes=4))


if __name__=='__main__':
    main()
