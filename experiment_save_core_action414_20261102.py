import hashlib
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module

def main():
 source=(ROOT/'nonmatching/save-core/20261102-action414/source.c').read_text();base='nonmatching/save-core/20261102-action414';variants={'pointer_declaration_swap':source.replace('    Row *clearRow;\n    Row *currentRow;','    Row *currentRow;\n    Row *clearRow;'),'current_pointer_early':source.replace('    Row *currentRow;\n','').replace('    u8 previousX;','    Row *currentRow;\n    u8 previousX;'),'clear_pointer_early':source.replace('    Row *clearRow;\n','').replace('    u8 previousX;','    Row *clearRow;\n    u8 previousX;'),'shared_phase_pointer':source.replace('clearRow','currentRow').replace('    Row *currentRow;\n    Row *currentRow;','    Row *currentRow;')};variants['clear_pointer_scoped']=source.replace('    Row *clearRow;\n','').replace('        clearRow = &native_data_021c4a04[clearIndex];','        Row *clearRow = &native_data_021c4a04[clearIndex];');variants['current_pointer_scoped']=source.replace('    Row *currentRow;\n','').replace('                currentRow = &native_data_021c4a04[rowIndex];','                Row *currentRow = &native_data_021c4a04[rowIndex];');variants['both_pointers_scoped']=variants['current_pointer_scoped'].replace('    Row *clearRow;\n','').replace('        clearRow = &native_data_021c4a04[clearIndex];','        Row *clearRow = &native_data_021c4a04[clearIndex];');variants['named_mode']=source.replace('    s32 clearIndex;','    const u32 requestMode = 5U;\n    s32 clearIndex;').replace('5U)','requestMode)');variants['shared_pointer_named_mode']=variants['shared_phase_pointer'].replace('    s32 clearIndex;','    const u32 requestMode = 5U;\n    s32 clearIndex;').replace('5U)','requestMode)');variants['clear_pointer_expression']=source.replace('&native_data_021c4a04[clearIndex]','native_data_021c4a04 + clearIndex');arm=measured_module('main')[1];rows=[]
 for label,text in variants.items():
  p=ROOT/base/(label+'.c');p.write_text(text);spec=importlib.util.spec_from_file_location('action414_'+label,ROOT/'evidence/application/save_core_historical_link_20261031.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.ENTRY,b.LENGTH,b.NAME,b.SOURCE=0x0206A584,1056,'native_main_0206a584',p.relative_to(ROOT).as_posix();b.FLAGS+=['-opt','speed'];b.WORK='work/save-core/action414/'+label
  try:row,body=b.build(arm[0x6A584:0x6A9A4]);row['variant']=label;rows.append(row);print(label,row['compiledBytes'],row['sameOffsetBytes'],row['exactByteEqual'],flush=True)
  except Exception as error:rows.append(dict(variant=label,error=str(error)));print(label,'ERROR',str(error)[:120],flush=True)
 p=ROOT/'evidence/attempts/save-core-action414-natural-lifetimes-20261102.json';p.write_text(json.dumps(dict(sourceCredit=0,sourceBytes=1056,rows=rows,generatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),limits=['Natural declaration/scope/reuse variants only;no padding,register assignments,assembly oropcode edits. Bounded10variants;genuine linked comparison is required andnative full-body execution remains unqualified.']),indent=2)+'\n')
if __name__=='__main__':main()
