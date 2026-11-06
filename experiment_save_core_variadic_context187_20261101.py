from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
import qualified_byte_variadic187_context_20261101 as Q
import draft_runtime as D


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    assert sys.version_info[:3]==(3,13,5)
    folder=ROOT/'evidence/generated/variadic-context187-20261101'
    folder.mkdir(parents=True,exist_ok=True)
    for name in ['input.s','context.c']:
        destination=folder/('baseline-'+name)
        assert destination.is_file(),('Missing committed analysis input',name)
    asm=(folder/'baseline-input.s').read_text()
    context=(folder/'baseline-context.c').read_text()
    assert sha((folder/'baseline-input.s').read_bytes())=='4f099fe7e30542f6d5f91234420caba2ddbaa1581d14126161a017bb42174349'
    assert sha((folder/'baseline-context.c').read_bytes())=='5d7b137051677b57abc5ba00005fd0801be5cde9a0e5f619f0997f0c78e7a26e'
    spec=dict(processor='arm9',program='',module='main',mode='arm',address=0x02066C64)
    typed,changes=Q.apply(context,spec)
    assert len(changes)==1
    tests=[]
    for label,source,view,edited in [('primary',context,spec,True),('thumb',context,dict(spec,mode='thumb'),True),('overlay_caller',context,dict(spec,module='ov001'),True),('arm7',context,dict(spec,processor='arm7'),False),('utility',context,dict(spec,program='utility'),False),('already_typed',typed,spec,False),('explicit_void',context.replace('func_0201d444();','func_0201d444(void);'),spec,False)]:
        result,receipt=Q.apply(source,view)
        assert bool(receipt)==edited
        if not edited:assert result==source
        tests.append(dict(name=label,changed=bool(receipt),passed=True))
    for label,key in [('source_pin','sourceSha256'),('native_pin','nativeSpanSha256')]:
        bad=dict(Q.CONTRACT,**{key:'00'*32})
        try:
            Q.validate(bad)
            raise RuntimeError('Bad pin accepted')
        except AssertionError as error:
            tests.append(dict(name=label,rejected=True,reason=str(error)))
    outputs=[]
    for label,source in [('before',context),('after',typed)]:
        ctx=folder/(label+'-context.c')
        ctx.write_text(source)
        command=[sys.executable,str(D.M2C),'--target','arm-mwcc-c','--comment-style','none','--no-cache','--valid-syntax','--context',str(ctx),'-f','func_02066c64',str(folder/'baseline-input.s')]
        process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONPATH=str(ROOT/'tools/m2c-python')),capture_output=True,text=True,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode==0,process.stderr
        result=folder/(label+'-output.c')
        result.write_text(process.stdout)
        outputs.append(dict(label=label,context=dict(path=ctx.relative_to(ROOT).as_posix(),sha256=sha(ctx.read_bytes())),output=dict(path=result.relative_to(ROOT).as_posix(),sha256=sha(result.read_bytes())),exitCode=process.returncode,command=command))
    before=(folder/'before-output.c').read_text()
    after=(folder/'after-output.c').read_text()
    assert 'func_0201d444(&sp7, &data_020de224);' in before
    expected='func_0201d444(&sp7, &data_020de224, M2C_FIELD(&data_021c36e8, s32 *, 0xC));'
    assert expected in after
    assert 'u8 sp7;' in after
    observation=dict(retainedConditionalNameWord=True,nativeCallerEvidence='evidence/matches/mechanics-save-20261101-lane-menu-resource-flows.json',
        qualifiedCallerNativeCaseDigest='222bca8474f5dd779da7874f6370887b830f74963b15e720b26fab548878238a',
        unresolvedReview=['Typed pointer formal infers single-byte sp7,not its17-byte native remaining-stack-span backing.','Variadic values remain untyped physical words;format-derived pointer casts and bounded buffers still require explicit source review.'])
    upstream={}
    for name in ['m2c/translate.py','m2c/arch_arm.py']:
        path=D.M2C.parent/name
        upstream[path.relative_to(ROOT).as_posix()]=sha(path.read_bytes())
    report=dict(schema=1,sourceCreditAdded=0,observation=observation,upstreamImplementation=upstream,helperSha256=sha((ROOT/'qualified_byte_variadic187_context_20261101.py').read_bytes()),contract=changes[0],controls=tests,outputs=outputs,
        limitations=['New m2c contexts only. No existing source/catalogue/framework edits. Variadic context can retain extra stale values;generated source and stack buffers remain hypotheses,not accepted source.'])
    path=ROOT/'evidence/lanes/save-core/variadic-context187-20261101.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(path.relative_to(ROOT),sha(path.read_bytes()))


if __name__=='__main__':
    main()
