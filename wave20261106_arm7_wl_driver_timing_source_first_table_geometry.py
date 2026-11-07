import re
import struct
from project import ROOT,sha256
from wave20261106_arm7_wl_driver_timing_source_first_tables import load


def execute():
    from wave20261106_arm7_wl_driver_timing_source_first_controls import compile_unit,function_body
    from wave20261106_arm7_wl_driver_timing_source_first_build import SOURCE,WORK
    positive=[];negative=[]
    for pin in load()['records']:
        tag=format(int(pin['caller'],0),'08x');symbol=pin['symbol'];expected=(pin['bytes'],pin['elementCount'],4 if pin['elementType']=='RATE_SET'else 2)
        def probe(label,change=None):
            target=WORK/'table-geometry'/pin['semanticName']/label;target.mkdir(parents=True,exist_ok=True);changed=0
            for path in (SOURCE/tag).glob('*'):
                if path.suffix not in ['.c','.h']:continue
                text=path.read_text()
                if change:
                    old='extern const '+pin['elementType']+' '+symbol+(';'if pin['elementType']=='RATE_SET'else'['+str(pin['elementCount'])+'] __attribute__((aligned(4)));')
                    if change=='count':new=old.replace('['+str(pin['elementCount'])+']','['+str(pin['elementCount']-1)+']')if pin['elementType']!='RATE_SET'else 'extern const unsigned char '+symbol+'[3];'
                    else:new=old.replace(pin['elementType'],'unsigned short'if pin['elementType']=='RATE_SET'else'unsigned long')
                    changed+=text.count(old);text=text.replace(old,new)
                (target/path.name).write_text(text)
            if change and changed!=1:raise ValueError('Actual C table declaration mutation not unique')
            source=target/'dimensions.c';obj=target/'dimensions.o';arrayExpression='sizeof('+symbol+')/sizeof('+symbol+'[0]),sizeof('+symbol+'[0])'if pin['elementType']!='RATE_SET'else'1,sizeof('+symbol+')';source.write_text('#include "main.c"\nunsigned long table_geometry[]={sizeof('+symbol+'),'+arrayExpression+'};\n');attempt=compile_unit(source,obj)
            if attempt['exitCode']:raise ValueError(('Actual typed table geometry rejected',attempt))
            actual=struct.unpack('<3I',function_body(obj,'table_geometry'))
            if actual!=expected:raise ValueError(('Actual table extent/count/element width differs',actual,expected))
            return dict(symbol=symbol,sourceSha256=sha256(source),objectSha256=sha256(obj),fullExtentBytes=actual[0],elementCount=actual[1],elementBytes=actual[2],storageCredit=0)
        positive.append(probe('positive'))
        for change in ['count','element-type']:
            try:probe(change,change)
            except ValueError as error:negative.append(dict(table=pin['semanticName'],case=change,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong actual compiler table declaration admitted')
    return dict(status='passed',sourceCredit=0,storageCredit=0,positive=positive,negativeControls=negative)
