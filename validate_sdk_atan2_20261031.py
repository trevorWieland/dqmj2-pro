from project import ROOT,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate
from sdk_atan2_native_20261031 import execute,ENTRY


def controls(original,rebuilt,table):
    source=(ROOT/'src/math/20261031_atan2/native_main_020028d8.c').read_text(encoding='utf-8')
    bindings={'native_fn_0200235c':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x0200235c'},'native_data_020d7fe0':{'module':'main','processor':'arm9','kind':'data','mode':'data','address':'0x020d7fe0'}}
    compiler.WORK=ROOT/'work/atan2-controls-20261031/compile';rows=[];actual_returns=0
    for name,text in [('wrong-table-shift',source.replace('>> 5','>> 6')),('wrong-quadrant-offset',source.replace('offset = 6434;','offset = 12868;'))]:
        path=ROOT/f'nonmatching/main-runtime/20261031/atan2-{name}.c';path.write_text(text,encoding='utf-8');found,_=compiler.compare(path,'main',2,'off',True);assert len(found)==1
        row=found[0];directory=ROOT/'work/atan2-controls-20261031'/name
        try:validate(row,bindings,directory=directory)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong C matched')
        payload=(directory/'caller.bin').read_bytes();assert len(payload)==440
        arm=bytearray(rebuilt);arm[ENTRY-0x02000000:ENTRY-0x02000000+440]=payload
        cases=[]
        for tag,(y,x) in enumerate([(1,2),(2,1),(-2,1),(1,-2),(0,1),(1,1),(8191,8192),(0,-1)]):
            native=execute(original,table,y,x,tag);wrong=execute(bytes(arm),table,y,x,tag,check=False);actual_returns+=2
            cases.append({'input':[y,x],'actualReturns':2,'nativeResult':native['result'],'wrongResult':wrong['result'],'rejected':not wrong['modelPassed'],'positiveControl':wrong['modelPassed']})
        rejected=sum(c['rejected'] for c in cases);positive=sum(c['positiveControl'] for c in cases);assert rejected and positive
        rows.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'objectSha256':row['objectSha256'],'completeCompiledCRealLinked':True,'exactByteRefusal':refusal,'rejections':rejected,'positiveControls':positive,'cases':cases})
    report={'passed':True,'sourceCredit':0,'actualTopLevelReturns':actual_returns,'functionResultProviders':0,'rejections':sum(r['rejections'] for r in rows),'positiveControls':sum(r['positiveControls'] for r in rows),'wholeSourceControls':rows}
    write_json(ROOT/'evidence/verification/sdk-atan2-controls-20261031.json',report);return report
