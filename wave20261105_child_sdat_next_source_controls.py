import copy
from project import ROOT,read_json,sha256
from wave20261105_child_sdat_next_source_codec import build
from wave20261105_child_sdat_next_source_generate import generate
from wave20261105_child_sdat_next_source_build import WORK,FLAGS,compile_unit,inspect_object


def semantic(values,layout):
    asset,symbol,text,expected,decoded=values[0];original=read_json(ROOT/asset['semanticSource']);rows=[]
    def reject(label,operation):
        try:operation()
        except (ValueError,AssertionError,OverflowError,IndexError) as error:rows.append(dict(case=label,address=asset['address'],rejected=True,reason=type(error).__name__+': '+str(error)))
        else:raise ValueError('Wrong semantic sound source retained exact target: '+label)
    def mutation(label,change,valid=False):
        value=copy.deepcopy(original);change(value['semantic'])
        def compare():
            payload,pad,_=build(value)
            if valid and payload+bytes(pad)!=expected:raise ValueError('Edited typed sound data changes original native/LZ agreement')
        reject(label,compare)
    for i in range(10):
        mutation('wave-'+str(i)+'-wrong-initial-index',lambda s,i=i:s['files'][2]['semantic']['waves'][i]['adpcm'].__setitem__('initialStepIndex',89))
        mutation('wave-'+str(i)+'-invalid-quantized-step',lambda s,i=i:s['files'][2]['semantic']['waves'][i]['adpcm']['signedQuantizedSteps'].__setitem__(0,0))
        mutation('wave-'+str(i)+'-wrong-loop-length',lambda s,i=i:s['files'][2]['semantic']['waves'][i].__setitem__('loopLengthWords',1))
        def edited_sample(s,i=i):
            samples=s['files'][2]['semantic']['waves'][i]['adpcm']['signedQuantizedSteps'];at=next(j for j,t in enumerate(samples) if abs(t)>1);samples[at]=1
        mutation('wave-'+str(i)+'-valid-quantized-sample-edit',edited_sample,True)
    mutation('MML-note-domain',lambda s:next(e for e in s['files'][0]['semantic']['commands']['events'] if e['kind']=='note').__setitem__('midiNote',128))
    mutation('MML-wrong-target-boundary',lambda s:next(e for e in s['files'][0]['semantic']['commands']['events'] if e['kind']=='jump').__setitem__('target',9999))
    mutation('MML-wrong-track',lambda s:next(e for e in s['files'][0]['semantic']['commands']['events'] if e['kind']=='open-track').__setitem__('track',16))
    mutation('MML-opaque-command-forbidden',lambda s:s['files'][0]['semantic']['commands']['events'][0].__setitem__('kind','opaque'))
    mutation('MML-valid-note-velocity-edit',lambda s:next(e for e in s['files'][0]['semantic']['commands']['events'] if e['kind']=='note').__setitem__('velocity',39),True)
    mutation('instrument-missing-wave',lambda s:s['files'][1]['semantic']['instruments'][2].__setitem__('waveIndex',10))
    mutation('instrument-envelope-domain',lambda s:s['files'][1]['semantic']['instruments'][0].__setitem__('attack',128))
    mutation('instrument-valid-envelope-edit',lambda s:s['files'][1]['semantic']['instruments'][0].__setitem__('attack',99),True)
    mutation('INFO-wrong-member-kind',lambda s:s['info']['banks'][0].__setitem__('fileId',0))
    mutation('INFO-missing-wave-slot',lambda s:s['info']['banks'][0]['waveArchives'].__setitem__(0,65535))
    mutation('SSAR-missing-bank',lambda s:s['files'][0]['semantic']['sequences'][0].__setitem__('bank',1))
    wrong=copy.deepcopy(original);wrong['measuredZeroAlignmentBytes']=2;reject('wrong-separate-storage-alignment',lambda:build(wrong))
    for label,key,value in [('wrong-program','program',''),('wrong-cpu','processor','arm7'),('wrong-module','module','main'),('wrong-base','base','0x2000004')]:
        wrong=copy.deepcopy(layout);wrong[key]=value;reject(label,lambda:generate(wrong))
    return dict(status='passed',sourceCredit=0,negativeControls=rows,validSemanticEditsMustNotRetainOriginalROMMatch=True)


def object_contract(sample,obj):
    asset,symbol,text,expected,decoded=sample;directory=WORK/'object-contract';directory.mkdir(parents=True,exist_ok=True);rows=[]
    for label,payload in [('extra-executable-function',text+'\nint unwanted_executable(void){return 1;}\n'),('mutable-data',text.replace('const unsigned char','unsigned char',1)),('allocated-pointer-relocation','extern const unsigned char outside[];\nconst unsigned char *const '+symbol+'['+str(len(expected)//4)+']={outside};\n')]:
        source=directory/(label+'.c');source.write_text(payload);candidate,attempt=compile_unit(source,directory/label)
        if attempt['exitCode']:raise ValueError('Meaningful negative sound data object did not compile')
        try:inspect_object(candidate,symbol,expected)
        except ValueError as error:rows.append(dict(case=label,rejected=True,reason=str(error),objectSha256=sha256(candidate),attempt=attempt))
        else:raise ValueError('Wrong data-object contract was admitted')
    try:inspect_object(obj,symbol+'_wrong',expected)
    except ValueError as error:rows.append(dict(case='wrong-object-symbol',rejected=True,reason=str(error)))
    else:raise ValueError('Wrong data-object symbol was admitted')
    return dict(status='passed',sourceCredit=0,negativeControls=rows)


def actual_frontend():
    directory=WORK/'frontend';directory.mkdir(parents=True,exist_ok=True);source=directory/'witness.c';source.write_text('int witness(void*p){int*value=p;return *value;}\n');rows=[]
    for language in ['c99','c++']:
        flags=list(FLAGS);flags[flags.index('-lang')+1]=language;obj,attempt=compile_unit(source,directory/language.replace('+','p'),flags)
        if (language=='c99')!=(attempt['exitCode']==0):raise ValueError('Actual pinned C99/C++ language witness failed')
        rows.append(dict(language=language,sourceSha256=sha256(source),objectSha256=sha256(obj) if not attempt['exitCode'] else None,attempt=attempt))
    return dict(status='passed',sourceCredit=0,positiveDataFrontend='explicit-c99',witnesses=rows,frontendWitnessExecutableObjectIsNotAssetOrFunctionCredit=True)
