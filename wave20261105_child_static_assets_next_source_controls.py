import copy
from project import ROOT,read_json,sha256
from wave20261105_child_static_assets_next_source_codec import build
from wave20261105_child_static_assets_next_source_generate import generate
from wave20261105_child_static_assets_next_source_build import WORK,COMPILER,FLAGS,compile_unit,inspect_object


def semantic(values,layout):
    rows=[]
    def reject(label,address,operation):
        try:operation()
        except (ValueError,AssertionError,OverflowError,IndexError) as error:rows.append(dict(case=label,address=address,rejected=True,reason=type(error).__name__+': '+str(error)))
        else:raise ValueError('Wrong semantic resource retained exact original target: '+label)
    for asset,symbol,text,expected,decoded in values:
        document=read_json(ROOT/asset['semanticSource']);changed=copy.deepcopy(document);s=changed['semantic'];kind=s['kind']
        if kind=='Nitro2D-4bpp-tiles':s['tiles'][0][0]='g'+s['tiles'][0][0][1:]
        elif kind=='Nitro2D-RGB555-palette':s['colors'][0]['b5']=32
        elif kind=='Nitro2D-text-screen':s['rows'][0][0]['palette']=16
        else:next(x for x in s['sections'] if x['kind']=='glyph-bitmap')['glyphs'][0]['rows'][0]='f'+next(x for x in s['sections'] if x['kind']=='glyph-bitmap')['glyphs'][0]['rows'][0][1:]
        reject('invalid-semantic-domain',asset['address'],lambda:build(changed));changed=copy.deepcopy(document);s=changed['semantic']
        if kind=='Nitro2D-4bpp-tiles':s['tiles'][0][0]=format(int(s['tiles'][0][0][0],16)^1,'x')+s['tiles'][0][0][1:]
        elif kind=='Nitro2D-RGB555-palette':s['colors'][0]['r5']^=1
        elif kind=='Nitro2D-text-screen':s['rows'][0][0]['verticalFlip']=not s['rows'][0][0]['verticalFlip']
        else:s['sections'][0]['lineFeed']+=1
        def compare():
            payload,pad,_=build(changed)
            if payload+bytes(pad)!=expected:raise ValueError('Edited semantics change target bytes or original compression choices')
        reject('valid-semantic-edit-loses-original-match',asset['address'],compare);changed=copy.deepcopy(document);changed['measuredZeroAlignmentBytes']=(changed['measuredZeroAlignmentBytes']+1)%4;reject('wrong-alignment-scalar',asset['address'],lambda:build(changed))
    for label,key,value in [('wrong-program','program',''),('wrong-cpu','processor','arm7'),('wrong-module','module','main'),('wrong-base','base','0x2000004')]:
        changed=copy.deepcopy(layout);changed[key]=value;reject(label,None,lambda:generate(changed))
    return dict(status='passed',sourceCredit=0,negativeControls=rows,validSemanticEditsMustNotRetainOriginalROMMatch=True)


def object_contract(sample,obj):
    asset,symbol,text,expected,decoded=sample;directory=WORK/'object-contract';directory.mkdir(parents=True,exist_ok=True);rows=[]
    for label,payload in [('extra-executable-function',text+'\nint unwanted_executable(void){return 1;}\n'),('mutable-data',text.replace('const unsigned char','unsigned char',1)),('allocated-pointer-relocation','extern const unsigned char outside[];\nconst unsigned char *const '+symbol+'['+str(len(expected)//4)+']={outside};\n')]:
        source=directory/(label+'.c');source.write_text(payload);candidate,attempt=compile_unit(source,directory/label)
        if attempt['exitCode']:
            if label!='allocated-pointer-relocation':raise ValueError('Meaningful negative data object did not compile')
            rows.append(dict(case=label,compileRejected=True,attempt=attempt));continue
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
