import subprocess
import sys
from project import ROOT,read_json,write_json,sha256
from wave20261106_gp_character_data_paths import EVIDENCE,assert_owned

FIELDS=['program','processor','module','kind','mode','formatKind','address','bytes','size','compiledBytes','nativeSymbol','source','sourceSha256','sourceDependencies','dataSourceDependencies','semanticSource','semanticSourceSha256','targetSha256','compiler','compilerSha256','compilerFlags','encodedAssetBytes','measuredZeroAlignmentBytes']


def projection(report):
    if report['functionMatched']!=0 or report['functionMatches']!=[]or report['dataMatchedBytes']!=3696 or len(report['dataMatches'])!=259:raise ValueError('Character packet function/data accounting differs')
    for row in report['dataMatches']:
        if row['ordinaryFunctionCredit']or row['executableSectionBytes']or row['allocatedZeroFillBytes']or row['relocations']or row['encodedAssetBytes']or row['measuredZeroAlignmentBytes']or not row['realLink']['exactDataAddress']or not row['realLink']['exactDataBytes']:raise ValueError('Character projection gained code, gap, BSS or unlinked data')
    return [{k:r[k]for k in FIELDS}for r in report['dataMatches']]


def main():
    assert_owned()
    if len(sys.argv)!=2:raise ValueError('Exact character canonical descriptor argument required')
    path=ROOT/sys.argv[1];descriptor=read_json(path);manifest=descriptor['sourceManifest']
    if not path.resolve().is_relative_to(EVIDENCE)or sha256(ROOT/manifest['path'])!=manifest['sha256']:raise ValueError('Exact canonical descriptor/source manifest differs')
    command=descriptor['originalProducer'];subprocess.run([sys.executable,str(ROOT/command[0]),*command[1:]],cwd=ROOT,check=True);report=read_json(ROOT/descriptor['originalReport'])
    if projection(report)!=descriptor['immutableDataProjection']:raise ValueError('Fresh original C/native/compiler/typed-object contracts changed')
    output=ROOT/descriptor['output']
    if not output.resolve().is_relative_to(ROOT/'evidence/matches'):raise ValueError('Character canonical output escaped report namespace')
    report.update(canonicalReportRefreshedFromFreshWorkerObjects=True,initializedDataTransport=dict(sourceCredit=0,descriptor=sys.argv[1],descriptorSha256=sha256(path),originalReport=descriptor['originalReport'],originalReportSha256=sha256(ROOT/descriptor['originalReport']),originalProducer=command,originalSourceManifestSha256=manifest['sha256'],dataContractsUnchanged=True,freshObjectAndLinkMetadataPublished=True))
    write_json(output,report);print(dict(dataObjects=259,initializedBytes=3696,functionCredit=0,canonicalReport=descriptor['output']),flush=True)


if __name__=='__main__':main()
