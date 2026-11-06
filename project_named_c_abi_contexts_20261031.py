import re
from project import ROOT,read_json,write_json,sha256
from project_matched_c_abi_contexts_20261031 import catalogue as canonical_catalogue,projected_type,split_parameters


def address(value):return int(value,0) if isinstance(value,str) else value


def catalogue():
    canonical,previous_rejections,build=canonical_catalogue();used={row['alias'] for row in canonical};rows=[];rejected=[];reports={};sources={}
    source_map=read_json(ROOT/'source-map.json')
    for row in source_map['matchedFunctions']:
        if row['processor']!='arm9' or row['module']!='main' or row.get('program'):continue
        alias=f"func_{address(row['address']):08x}"
        if alias in used:continue
        source=row['sourceUnit'];path=ROOT/source
        if path.suffix.lower() not in ['.c','.cpp']:continue
        if source not in sources:sources[source]=(path.read_text(encoding='utf-8-sig'),sha256(path))
        text,digest=sources[source];assert digest==row['sourceSha256']
        evidence=row['evidence']
        if evidence not in reports:reports[evidence]=read_json(ROOT/evidence)
        report=reports[evidence];candidates=[]
        for entry in report.get('matches',report.get('functionMatches',[])):
            if address(entry.get('address'))!=address(row['address']):continue
            if entry.get('source',report.get('source'))!=source:continue
            if entry.get('sourceSha256',report.get('sourceSha256'))!=digest:continue
            if entry.get('name'):candidates.append(entry['name'])
        names=set(candidates)
        if len(names)!=1:
            rejected.append(dict(address=row['address'],source=source,reason='No unique source-hash-qualified matching C symbol'));continue
        name=names.pop();pattern=r'^\s*([^;{}\n]+?)\s+'+re.escape(name)+r'\s*\(([^;{}]*)\)\s*\{';definitions=list(re.finditer(pattern,text,re.M))
        if len(definitions)!=1:
            rejected.append(dict(address=row['address'],source=source,sourceFunction=name,reason='No unique ordinary C definition'));continue
        definition=definitions[0];returns=projected_type(definition[1]);raw=definition[2].strip()
        if raw=='void':parameters=[]
        elif not raw:
            rejected.append(dict(address=row['address'],source=source,sourceFunction=name,reason='Unspecified parameter list'));continue
        else:parameters=[projected_type(part,parameter=True) for part in split_parameters(raw)]
        if returns is None or any(part is None for part in parameters):
            rejected.append(dict(address=row['address'],source=source,sourceFunction=name,reason='Unsupported scalar, callback or aggregate type'));continue
        prototype=f"extern {returns} {alias}({', '.join(parameters) if parameters else 'void'});"
        rows.append(dict(processor='arm9',module='main',program='',mode=row['mode'],address=row['address'],alias=alias,returnType=returns,parameterTypes=parameters,source=source,sourceFunction=name,sourceSha256=digest,matchingReport=evidence,matchingReportSha256=sha256(ROOT/evidence),contextPrototype=prototype,sourceCredit=0,callerNativeValidationRequired=True,qualification='Projection of a source-hash-qualified selected C symbol; opaque ARM32 pointers; no historical signature or complete native call-domain claim'))
    return canonical,rows,rejected,build


def main():
    canonical,rows,rejected,build=catalogue();create=next(row for row in rows if address(row['address'])==0x0206271C)
    assert create['sourceFunction']=='saved_record_create' and create['returnType']=='u32' and create['parameterTypes']==['int','int']
    write_json(ROOT/'evidence/attempts/projected-named-c-abi-contexts-20261031.json',dict(buildSha256=build,sourceMapSha256=sha256(ROOT/'source-map.json'),generatorSha256=sha256(__file__),sourceCredit=0,canonicalContracts=len(canonical),additionalContracts=rows,contracts=canonical+rows,skipped=rejected,calibrationSavedRecordCreate=create,limitations=['Matching report symbol names constrain new generated caller hypotheses; no existing source/object/registry is edited','Only exact source-hash-qualified named definitions are added; unknown, callback and aggregate declarations are skipped','Pointers retain target32-bit ABI width with erased pointee/depth; complete object extents and semantics remain unqualified','Native call-boundary observations and genuine compiler/linker comparisons remain necessary for every new caller']))
    print(dict(canonicalContracts=len(canonical),additionalContracts=len(rows),skipped=len(rejected),savedRecordCreatePrototype=create['contextPrototype'],sourceCredit=0))


if __name__=='__main__':main()
