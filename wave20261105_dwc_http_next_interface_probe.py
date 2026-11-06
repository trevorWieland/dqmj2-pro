import importlib,re,shutil
from project import ROOT,read_json,write_json,sha256
import match_runtime
from elftools.elf.elffile import ELFFile
LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next'
CALLEES={'native_fn_020987b0':'second/020987b0/020987b0.c','native_fn_020983d0':'first/020983d0/020983d0.c'}
def extent(row):
 with(ROOT/row['object']).open('rb')as stream:
  elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==row['name']);start=symbol['st_value']&~1;return elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']],dict(binding=symbol['st_info']['bind'],type=symbol['st_info']['type'],bytes=symbol['st_size'])
def main():
 debt=read_json(LANE/'implicit-interface-debt-v1.json');results=[];callee_proofs=[]
 for name,suffix in CALLEES.items():
  path=ROOT/'src/runtime/parallel_wave20261105/dwc-http-next'/suffix;assert re.search(r'void\s+native_main_',path.read_text());callee_proofs.append(dict(alias=name,source=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),declaration=path.read_text().splitlines()[1].split('{')[0],sourceReturnType='void',argumentCount=1,argumentView='DWCHttp pointer word',calleeSourceCreditInCallerPacket=0))
 selected=[item for item in debt['findings']if item['packet']in ['fifth','sixth','seventh']and item['callee']in CALLEES]
 assert len(selected)==5
 for item in selected:
  packet,address=item['packet'],int(item['caller'],0);directory=ROOT/f'work/w5dh/{packet}/interface-prototype-probe/{address:08x}';assert not directory.exists();assert directory.is_relative_to(ROOT/f'work/w5dh/{packet}');directory.mkdir(parents=True)
  source=ROOT/item['source']['path'];assert sha256(source)==item['source']['sha256'];copy=directory/source.name;shutil.copyfile(source,copy)
  for pin in item['headers']:assert sha256(ROOT/pin['path'])==pin['sha256'];shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
  builder=importlib.import_module('wave20261105_dwc_http_next_'+packet+'_build').build;baseline,b0=builder(copy,directory/'baseline');before,s0=extent(baseline)
  header=directory/'context.h';old=header.read_text();declaration='extern void '+item['callee']+'(DWCHttp*);';assert not re.search(r'\b'+item['callee']+r'\s*\(',old);header.write_text(old+'\n'+declaration+'\n');typed,b1=builder(copy,directory/'typed');after,s1=extent(typed)
  assert before==after and s0==s1 and baseline['relocations']==typed['relocations']and b0==b1 and typed['realLink']['exactCallerBytes'];results.append(dict(caller=item['caller'],packet=packet,originalSource=item['source'],originalHeaderPins=item['headers'],addedDeclaration=declaration,privateHeaderSha256=sha256(header),completeCompilerObjectFunctionBytesIdentical=True,allOriginalRelocationSignaturesIdentical=True,callerSymbolBindingTypeExtentIdentical=True,fullGenuineNativeLinkedSpanIdentical=True,rawObjectFilesByteIdentical=sha256(ROOT/baseline['object'])==sha256(ROOT/typed['object']),baselineObjectSha256=baseline['objectSha256'],typedObjectSha256=typed['objectSha256'],nativeBytes=typed['bytes'],sourceOrExecutionCredit=0))
 body=dict(schemaVersion=1,status='private-zero-byte-interface-probe-only',allPassed=True,qualifiedCalleeSourceDeclarations=callee_proofs,callerProbes=results,callers=5,bytesAdded=0,frozenSourceHeaderInputHelperReadyUnchanged=True,sharedCfgRegistryAndAcceptanceUnchanged=True,distinction='Actual qualified complete imported callee sources declare void(one DWCHttp pointer),whereas old caller contexts use implicit int through MW extensions and merely ignore returned R0. This private header-only probe proves exact complete caller function bytes/symbols/relocations and genuine links after adding correct prototypes; whole object containers may differ in debug/type metadata.',remainingUnqualifiedLibraryDeclaration=[item for item in debt['findings']if item['callee']not in CALLEES],proposedNextAction='Coordinator-owned zero-byte explicit-interface migration after current gates; rerun standard copied-root/shared validation before replacing any frozen selected context.',sourceOrExecutionCredit=0)
 p=LANE/'qualified-Http-interface-probe.json';assert not p.exists();write_json(p,body);print(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p),callers=5,bytesAdded=0))
if __name__=='__main__':main()
