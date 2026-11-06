from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighth_controls import projection_abi
from wave20261105_socket_thumb_next_sixteenth_bindings import negative_controls
from wave20261105_socket_thumb_next_sixteenth_callbacks import execute as callback_controls

REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/reference-manifest.json', 'sha256': '30750198e39a2e303f7f6e2843345e1bf6938f146906fa0f8d128ad4c804c260'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_shutdown.c', 'sha256': '4b646c03b7824210f878520b109a5945848b7f019818f4fc79718f2758660489'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_close.c', 'sha256': 'd5283509ab77a14a3eb96424652b6c3ce87e730690944212b2ca2c5648fa6725'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_cleanup.c', 'sha256': 'a44ba6e6407efb877eec5cce069cf199f417b9b27de5d4438733be86389e60f2'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/reference-manifest.json', 'sha256': '24253dc196d195ee4f546c2f68a9d29918beaa838116e93e2f73ec7c5e430463'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/message.h', 'sha256': 'a478ca5e02f830554b8df9266d264b758c3eca4f8aee9e6ced15728e718c674c'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/thread.h', 'sha256': '50c9abbb9f95c8eccb2ccddc2f01c46f682c241f4702d492fed35ad37fb24742'}]


def execute(rows):
    directory=ROOT/'work/w5st/sixteenth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/sixteenth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual socket/status/receive geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,recvPrefix276=True,udpHeader12=True,stateWord16=True,resultWord32=True,cpsPrefix100=True,threadSpecific196=True,mutex224=True,noConsume254=True)
    wrong=[]
    for label,old,new in [('pipe-thread-offset','u8 queue0[32]','u8 queue0[28]'),('pipe-mutex-offset','u8 thread20[192]','u8 thread20[188]'),('receive-count-width','volatile u16 size108;','volatile u32 size108;'),('socket-state-width','volatile s16 state70;','volatile s32 state70;')]:
        if original.count(old)!=1:raise ValueError('Actual socket layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong socket layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public socket/source/type comparison changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),indirectInterfaces=callback_controls(rows),wrongRuntimeTags=runtime_tags(rows),publicReferences=REFERENCES,limits=['Native source/private types are independently compiled/genuinely linked. Public implementation/layout correspondence does not prove exact SDK version, full original declarations/storage, network/thread/game/platform behavior. Controlled read-ordinal data updates are unit fixtures, not original hardware observations.'])



def runtime_tags(rows):
    from wave20261105_socket_thumb_next_sixteenth_models import fixtures,scenario
    from wave20261105_socket_thumb_next_sixteenth_execution import run
    import link_runtime_unit as L
    unused,main,unused=L.measured_module('main');bad=[]
    row=next(r for r in rows if int(r['address'],0)==0x0208fdc8);name='0208fdc8';path=(ROOT/row['realLink']['linkedElf']).parent/'caller.bin'
    if sha256(path)!=row['outputSha256']:raise ValueError('Actual cleanup runtime-tag caller bytes changed')
    body=path.read_bytes()
    for site in [0x0208fe0e,0x0208fe64]:
        for mode in ['arm','thumb']:
            fixture=next(f for i,f in enumerate(fixtures(name)) if ((releases:=[a for a in scenario(name,f,i)['actions'] if a['kind']=='release']) and releases[0]['mode']==mode and releases[0]['returnEntry']==((site+2)|1)))
            result=run(row,body,dict(fixture,_wrongTag=True),main)
            if not result['modelFailures'] or result['actualTopReturn'] or not result['rejectedAtObservedProtocolBoundary'] or result['calls'][-1]['mode']==mode:raise ValueError('Wrong controlled release runtime tag not rejected at exact mode boundary')
            bad.append(dict(caller=row['address'],site=hex(site),declaredFreshProviderMode=mode,actualMode=result['calls'][-1]['mode'],rejected=True,actualCallerReturn=False,originalCalleeBodiesExecuted=0,fixture=fixture,result=result))
    return bad
