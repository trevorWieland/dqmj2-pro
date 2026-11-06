from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighth_controls import projection_abi
from wave20261105_socket_thumb_next_twelfth_bindings import negative_controls
from wave20261105_socket_thumb_next_twelfth_callbacks import execute as callback_controls

REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-read/manifest.json', 'sha256': 'ee84f2b3cd60b635fb08c123a9f54029375df0a2fcfe26ebc70562e0ed75dae4'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-read/libraries/soc/src/socl_read.c', 'sha256': 'cf7fb830b1232df2af32116e3b0a48df70185f31ad4e67ec07f2049f770fd929'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/libraries/soc/src/socl_command.c', 'sha256': '2b023bcaeb5db6f66fdc81cefe768cbf2470d9b109edaa48c936f54f061f77a0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/reference-manifest.json', 'sha256': '6f06b4fd80ce55d40bb2472aeaf0c43110139d87d7f70bc602755469076d97c5'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/include/nitroWiFi/cps.h', 'sha256': 'a50f467431d9e3334b6c5d63428b3cf979f9373d84fb0b491de6bfbe75b1895d'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/reference-manifest.json', 'sha256': '24253dc196d195ee4f546c2f68a9d29918beaa838116e93e2f73ec7c5e430463'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/message.h', 'sha256': 'a478ca5e02f830554b8df9266d264b758c3eca4f8aee9e6ced15728e718c674c'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/thread.h', 'sha256': '50c9abbb9f95c8eccb2ccddc2f01c46f682c241f4702d492fed35ad37fb24742'}]


def execute(rows):
    directory=ROOT/'work/w5st/twelfth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/twelfth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual socket/status/receive geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,recvPrefix276=True,udpHeader12=True,stateWord16=True,resultWord32=True,cpsPrefix100=True,threadSpecific196=True,mutex224=True,noConsume254=True)
    wrong=[]
    for label,old,new in [('CPS-port-offset','u8 opaque9;','u8 opaque9[3];'),('receive-specific-offset','u8 opaque0[196]','u8 opaque0[192]'),('queue-size-word-width','volatile u16 size108;','volatile u32 size108;'),('UDP-payload-offset','u16 size4;','u32 size4;'),('config-function-offset','u8 opaque0[24];void *(*allocate18)','u8 opaque0[28];void *(*allocate18)')]:
        if original.count(old)!=1:raise ValueError('Actual socket layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong socket layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public socket/source/type comparison changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),indirectInterfaces=callback_controls(rows),wrongRuntimeTags=runtime_tags(rows),publicReferences=REFERENCES,limits=['Native source/private types are independently compiled/genuinely linked. Public implementation/layout correspondence does not prove exact SDK version, full original declarations/storage, network/thread/game/platform behavior. Controlled read-ordinal data updates are unit fixtures, not original hardware observations.'])



def runtime_tags(rows):
    from wave20261105_socket_thumb_next_twelfth_models import fixtures,scenario
    from wave20261105_socket_thumb_next_twelfth_execution import run
    import link_runtime_unit as L
    unused,main,unused=L.measured_module('main');bad=[]
    for row in rows:
        name=format(int(row['address'],0),'08x');kind='release' if name=='0208f578' else 'allocate';path=(ROOT/row['realLink']['linkedElf']).parent/'caller.bin'
        if sha256(path)!=row['outputSha256']:raise ValueError('Actual runtime-tag caller bytes changed')
        body=path.read_bytes()
        for mode in ['arm','thumb']:
            fixture=next(f for i,f in enumerate(fixtures(name)) if any(a['kind']==kind and a['mode']==mode for a in scenario(name,f,i)['actions']))
            result=run(row,body,dict(fixture,_wrongTag=kind),main)
            if not result['modelFailures'] or result['actualTopReturn'] or not result['rejectedAtObservedProtocolBoundary'] or result['calls'][-1]['mode']==mode:raise ValueError('Wrong actual controlled callable tag not rejected at mode boundary')
            bad.append(dict(caller=row['address'],kind=kind,declaredFreshProviderMode=mode,actualMode=result['calls'][-1]['mode'],rejected=True,actualCallerReturn=False,originalCalleeBodiesExecuted=0,fixture=fixture,result=result))
    return bad
