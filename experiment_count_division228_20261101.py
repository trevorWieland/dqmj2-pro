from pathlib import Path
import importlib.util,json,sys
sys.path[:0]=['.','evidence/application','deps/native']
from link_runtime_unit import measured_module
arm=measured_module('main')[1];folder=Path('nonmatching/save-core/20261101-count-division228');folder.mkdir(parents=True,exist_ok=True)
base='typedef unsigned char u8;\ntypedef signed char s8;\ntypedef unsigned int u32;\ntypedef signed int s32;\n#define FIELD(value,type,offset) (*(type)((u8 *)(value)+(offset)))\nextern u8 native_data_021c4f60[];\n'
rows=[]
for name,decl,calc in [('cached','s8 result;\n    s32 count;','count=FIELD(native_data_021c4f60,s32 *,0x14);\n    result=count/14;\n    if(count%14)result++;'),('count_first','s32 count;\n    s8 result;','count=FIELD(native_data_021c4f60,s32 *,0x14);\n    result=count/14;\n    if(count%14)result++;'),('direct','s8 result;','result=FIELD(native_data_021c4f60,s32 *,0x14)/14;\n    if(FIELD(native_data_021c4f60,s32 *,0x14)%14)result++;'),('explicit_cast','s32 count;\n    s8 result;','count=FIELD(native_data_021c4f60,s32 *,0x14);\n    result=(s8)(count/14);\n    if(count%14!=0)result=(s8)(result+1);'),('named_quotient','s8 result;\n    s32 count;\n    s32 quotient;','count=FIELD(native_data_021c4f60,s32 *,0x14);\n    quotient=count/14;\n    result=quotient;\n    if(count-quotient*14)result++;')]:
 path=folder/(name+'.c');path.write_text(base+'u32 native_main_02070f44(void) {\n    '+decl+'\n    if(FIELD(native_data_021c4f60,s8 *,0x2F)!=0)return 1;\n    '+calc+'\n    if(result==0)result++;\n    return (u32)result;\n}\n')
 for speed in [False,True]:
  spec=importlib.util.spec_from_file_location('count228_'+name+str(speed),'evidence/application/save_core_historical_link_20261031.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
  b.ENTRY,b.LENGTH,b.NAME,b.SOURCE,b.WORK=0x02070F44,120,'native_main_02070f44',path.as_posix(),'work/save-core/count-division228/'+name+str(speed)
  if speed:b.FLAGS=[*b.FLAGS,'-opt','speed']
  try:
   row,body=b.build(arm[0x70F44:0x70F44+120]);print(name,speed,row['compiledBytes'],row['sameOffsetBytes'],row['exactByteEqual'])
  except Exception as error:row=dict(source=path.as_posix(),flags=b.FLAGS,failure=str(error),sourceCredit=0);print(name,speed,str(error))
  rows.append(row)
Path('evidence/lanes/save-core/count-division228-20261101.json').write_text(json.dumps(rows,indent=2)+'\n')
