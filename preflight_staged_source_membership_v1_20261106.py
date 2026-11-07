import argparse
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256


def membership(package_name):
    package=read_json(ROOT/package_name);allowed=set(package.get('extra',[]))|set(package.get('traces',[]))
    for name in package['manifests']:allowed.update(r['path'].replace(chr(92),'/')for r in read_json(ROOT/name)['files'])
    for batch in read_json(ROOT/'recovery.json')['batches']:allowed.update(batch.get('sourceHashes',{}))
    name='evidence/verification/cohort'+str(package['cohort'])+'-captured-oracle-closure-20261031.json'
    if(ROOT/name).is_file():allowed.update(read_json(ROOT/name)['sourceAndEvidenceHashes'])
    return package,allowed


def suspect(names,allowed):
    findings=[]
    for name in names:
        if not name.startswith('src/')or Path(name).suffix.lower()not in {'.c','.h','.cpp','.inc','.s'}or name in allowed:continue
        previous=subprocess.run(['git','cat-file','-e','HEAD:'+name],cwd=ROOT,capture_output=True)
        if previous.returncode:findings.append(name)
    return sorted(findings)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('package');parser.add_argument('--output',required=True);args=parser.parse_args()
    package,allowed=membership(args.package)
    names=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines();findings=suspect(names,allowed)
    output=dict(advisory=True,sourceCredit=0,cohort=package['cohort'],package=args.package,packageSha256=sha256(ROOT/args.package),suspectedUnselectedNewStagedSources=findings,clean=not findings,readOnlyIndex=True,originalStagingWhitespaceAndClosureGuardsUnchanged=True,generatorSha256=sha256(__file__),limits=['Early diagnostic only: a newly discovered legitimate static oracle input can require explicit review','This does not replace original staging, whitespace classification or source/oracle audits'])
    write_json(ROOT/args.output,output);print(dict(clean=not findings,suspectedUnselectedSources=len(findings),readOnlyIndex=True))
    if findings:raise SystemExit(1)


if __name__=='__main__':main()
