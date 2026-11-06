from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighth_controls import projection_abi
from wave20261105_socket_thumb_next_thirteenth_bindings import negative_controls

REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-read/manifest.json', 'sha256': 'ee84f2b3cd60b635fb08c123a9f54029375df0a2fcfe26ebc70562e0ed75dae4'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-read/libraries/soc/src/socl_read.c', 'sha256': 'cf7fb830b1232df2af32116e3b0a48df70185f31ad4e67ec07f2049f770fd929'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/libraries/soc/src/socl_command.c', 'sha256': '2b023bcaeb5db6f66fdc81cefe768cbf2470d9b109edaa48c936f54f061f77a0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/reference-manifest.json', 'sha256': '6f06b4fd80ce55d40bb2472aeaf0c43110139d87d7f70bc602755469076d97c5'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/include/nitroWiFi/cps.h', 'sha256': 'a50f467431d9e3334b6c5d63428b3cf979f9373d84fb0b491de6bfbe75b1895d'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/reference-manifest.json', 'sha256': '24253dc196d195ee4f546c2f68a9d29918beaa838116e93e2f73ec7c5e430463'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/message.h', 'sha256': 'a478ca5e02f830554b8df9266d264b758c3eca4f8aee9e6ced15728e718c674c'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/thread.h', 'sha256': '50c9abbb9f95c8eccb2ccddc2f01c46f682c241f4702d492fed35ad37fb24742'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-write/reference-manifest.json', 'sha256': '25503394ede91e8a3b316084373a56a9142383eb492cf7a726882ccf92d10a9b'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-write/libraries/soc/src/socl_write.c', 'sha256': '37ec73c7b81978cc58a9d2db4491cb0540de5b5e3f9389526eb7b8e051655cb7'}]


def execute(rows):
    directory=ROOT/'work/w5st/thirteenth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/thirteenth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual socket/status/receive geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,recvPrefix276=True,udpPrefix12=True,sendPrefix272=True,stateWord16=True,resultWord32=True,cpsPrefix100=True,threadSpecific196=True,mutex224=True,noConsume254=True)
    wrong=[]
    for label,old,new in [('ring-index-width','volatile u16 in100;','volatile u32 in100;'),('send-mutex-size','u8 mutexE0[24];u32 sizeF8;','u8 mutexE0[20];u32 sizeF8;'),('ring-size-word-width','u32 sizeF8;','u16 sizeF8;'),('native-send-size-width','u32 sendSize48;','u16 sendSize48;')]:
        if original.count(old)!=1:raise ValueError('Actual socket layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong socket layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public socket/source/type comparison changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),incomingFormalHome=incoming_formal_control(rows),publicReferences=REFERENCES,limits=['Native source/private types are independently compiled/genuinely linked. Public implementation/layout correspondence does not prove exact SDK version, full original declarations/storage, network/thread/game/platform behavior. Controlled read-ordinal data updates are unit fixtures, not original hardware observations.'])



def verify_formal(contract,row,image):
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    expected=dict(caller=0x0208f7e4,frameBytes=56,store=0x0208f7ee,argumentIndex=4,offsetFromIncomingSP=0,bytes=4)
    if contract!=expected or int(row['address'],0)!=expected['caller']:raise ValueError('Exact incoming formal home contract differs')
    body=image[expected['caller']-0x02000000:expected['caller']-0x02000000+row['bytes']]
    if C.sha(body)!=row['targetSha256']:raise ValueError('Original incoming formal store function changed')
    instructions={i.address:(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(body,expected['caller'])}
    measured={0x0208f7e4:('push','{r4, r5, r6, r7, lr}'),0x0208f7e6:('sub','sp, #0x24'),0x0208f7ea:('ldr','r0, [sp, #0x38]'),0x0208f7ee:('str','r0, [sp, #0x38]')}
    if any(instructions.get(address)!=pair for address,pair in measured.items()):raise ValueError('Actual original frame/load/store formal flow differs')
    return dict(status='passed',sourceCredit=0,contract=contract,instructions=[dict(address=hex(a),mnemonic=m,operands=o) for a,(m,o) in measured.items()],limits=['Callee may overwrite its exact incoming fifth by-value argument home SP+0 with the same word. This permits only the measured4B slot, not a broader frame; positive runtime also verifies its final value.'])


def incoming_formal_control(rows):
    from wave20261105_socket_thumb_next_thirteenth_bindings import inputs
    value,image,inventory,records,imports=inputs();row=next(r for r in rows if int(r['address'],0)==0x0208f7e4)
    contract=dict(caller=0x0208f7e4,frameBytes=56,store=0x0208f7ee,argumentIndex=4,offsetFromIncomingSP=0,bytes=4);positive=verify_formal(contract,row,image);bad=[]
    for key,wrong in [('caller',0x0208f7e6),('frameBytes',52),('store',0x0208f7ec),('argumentIndex',5),('offsetFromIncomingSP',4),('bytes',8)]:
        variant=dict(contract);variant[key]=wrong
        try:verify_formal(variant,row,image)
        except ValueError as error:bad.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong incoming formal home admitted')
    changed=bytearray(image);changed[contract['store']-0x02000000]^=1
    try:verify_formal(contract,row,bytes(changed))
    except ValueError as error:bad.append(dict(case='original-store-code',rejected=True,reason=str(error)))
    else:raise ValueError('Changed incoming formal store admitted')
    return dict(positive=positive,negative=bad)
