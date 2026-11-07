import struct
from unittest.mock import patch
import wave20261105_arm7_boundary_next_flow as original
ORIGINAL_SWITCH=original.switch_witness


def bounded_switch(image,base,address,engine):
    existing=ORIGINAL_SWITCH(image,base,address,engine)
    if existing:return existing
    if address<base+4 or address+12>base+len(image):return None
    compare,dispatch,default=struct.unpack_from('<III',image,address-base-4)
    if compare&0xfff0f000!=0xe3500000 or dispatch&0xfffffff0!=0x908ff100 or default&0xff000000!=0xea000000:return None
    register=dispatch&15
    if register>=15 or(compare>>16)&15!=register:return None
    rotate=((compare>>8)&15)*2;value=compare&255;maximum=((value>>rotate)|(value<<(32-rotate)))&0xffffffff if rotate else value
    if maximum>255:return None
    addresses=[address+8+i*4 for i in range(maximum+1)]
    if addresses[-1]+4>base+len(image):return None
    words=[struct.unpack_from('<I',image,a-base)[0]for a in addresses]
    if any(word&0xff000000!=0xea000000 for word in words):return None
    return dict(dispatch=hex(address),encoding='AL CMP immediate / LS ADD PC,PC,index LSL2 / AL B default / actual AL B case instructions',compareAddress=hex(address-4),compareWord=hex(compare),dispatchWord=hex(dispatch),defaultAddress=hex(address+4),defaultWord=hex(default),indexRegister='r'+str(register),indexBound='unsigned index <= actual immediately preceding CMP maximum',unsignedInputBits=32,lower=0,upper=maximum,indices=maximum+1,tableEntryMode='arm',tableEncoding='actual unconditional ARM branch instructions, not data addresses',tableAddresses=[hex(a)for a in addresses],tableWords=[hex(w)for w in words],criticalLinearFlowStart=hex(address-4),criticalLinearFlowEnd=hex(address+4),requiresNoMiddleControlFlowEntry=True,sourceCredit=0)


def analyze(image,base,entry):
    with patch.object(original,'switch_witness',bounded_switch):return original.analyze(image,base,entry)


def controls(image,base,dispatch):
    import copy
    import match_runtime
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
    engine=Cs(CS_ARCH_ARM,CS_MODE_ARM);engine.detail=True;positive=bounded_switch(image,base,dispatch,engine)
    if positive is None:raise ValueError('Actual native strict unsigned bounded switch absent')
    results=[];at=dispatch-base
    for label,offset,change in [('conditional-CMP',at-4,lambda w:w^0x10000000),('CMP-without-flags',at-4,lambda w:w^(1<<20)),('different-index',at,lambda w:w^1),('wrong-index-shift',at,lambda w:w^(1<<7)),('wrong-condition',at,lambda w:w^0x10000000),('default-call',at+4,lambda w:w|(1<<24)),('table-call',at+8,lambda w:w|(1<<24)),('oversized-index',at-4,lambda w:(w&~4095)|0x401)]:
        mutated=bytearray(image);word=struct.unpack_from('<I',mutated,offset)[0];struct.pack_into('<I',mutated,offset,change(word))
        if bounded_switch(bytes(mutated),base,dispatch,engine)is not None:raise ValueError('Malformed actual guard/dispatch/table admitted:'+label)
        results.append(dict(case=label,rejected=True,actualOriginalBytesUnchanged=True))
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=results,originalAnalyzerFileChanged=False,productionRoutingChanged=False)
