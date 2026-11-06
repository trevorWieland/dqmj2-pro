import re
from project import ROOT,read_json,write_json,sha256
from wave20261102_child_fourth_types import units,write_closed

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/sdk'
WORK=ROOT/'work/w5ml/sdk/adapted'


def combined(path):
    text=path.read_text()
    return re.sub(r'^#include "([^"<>]+)"$',lambda m:(path.parent/m[1]).read_text(),text,flags=re.M)


def main():
    imports=read_json(LANE/'original-imports.json');closed=read_json(LANE/'closed-reference-probes.json');results=[]
    declarations={'sStrmThread':'extern NNSSndStrmThread native_data_020f5040;', 'sDecodeBufferMutex':'extern OSMutex native_data_020f4c9c;', 'cAdpcmIndexTable':'extern const s8 native_data_020d91a0[16];','cAdpcmStepSizeTable':'extern const s16 native_data_020d91b0[89];'}
    renamed={key:imports['mapping'][key]['newSymbol'] for key in imports['mapping'] if not key.startswith('_')}
    renamed.update(sStrmThread='native_data_020f5040',sDecodeBufferMutex='native_data_020f4c9c',cAdpcmIndexTable='native_data_020d91a0',cAdpcmStepSizeTable='native_data_020d91b0',sDecodeBuffer='native_data_020f4c84.decodeBuffer',sPrepareThread='native_data_020f4c84.prepareThread')
    for item in closed['results']:
        name=item['referenceFunction'];address=int(item['address'],0);primary='native_main_'+format(address,'08x');text=combined(ROOT/item['source']);pieces=[];small_globals=bool(re.search(r'\b(?:sDecodeBuffer|sPrepareThread)\b',text))
        for entity_name,entity in units(text):
            if entity_name is None:
                if re.search(r'\bstatic\b[^;]*\bsDecodeBuffer\b',entity):continue
                handled=False
                for symbol,replacement in declarations.items():
                    if re.search(r'\bstatic\b[\s\S]*\b'+symbol+r'\s*(?:\[|;|=)',entity):pieces.append(replacement+'\n');handled=True;break
                if handled:continue
            if entity_name==name and small_globals:pieces.append('typedef struct J2StreamGlobals {int initialized;struct NNSSndStrmThread *prepareThread;u8 *decodeBuffer;} J2StreamGlobals;\nextern J2StreamGlobals native_data_020f4c84;\n')
            entity=re.sub(r'\b'+re.escape(name)+r'\b',primary,entity)
            tokens={old:new for old,new in renamed.items() if old!=name}
            if tokens:entity=re.sub(r'\b(?:'+ '|'.join(re.escape(old) for old in sorted(tokens,key=len,reverse=True))+r')\b',lambda m:tokens[m[0]],entity)
            pieces.append(entity)
        directory=WORK/format(address,'08x');path=directory/(format(address,'08x')+'.c');headers=write_closed('\n'.join(pieces),primary,path)
        for header in headers:
            if len(header.read_text().splitlines())>500:header.write_text('\n'.join(line for line in header.read_text().splitlines() if line.strip())+'\n')
        row=dict(referenceFunction=name,address=hex(address),bytes=item['bytes'],source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),headers=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in headers],sourceMethod='Closed comparative ordinary C; exact measured original function/import names; imported storage declarations replace original comparative storage, small BSS group explicit measured0/4/8 view',sourceAndStorageCredit=0)
        results.append(row);print(name,hex(address),len(headers),flush=True)
    write_json(LANE/'adapted-source-inputs.json',dict(schemaVersion=1,immutableInputManifest=True,originalImports=dict(path=(LANE/'original-imports.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'original-imports.json')),entries=results,sourceAndStorageCredit=0))


if __name__=='__main__':main()
