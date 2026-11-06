import random
import struct

WORD,OBJECT,CLEAR,CONTEXT=0x021BD508,0x021C378C,0x021BCC0C,0x02217BE0


def recipes():
    values=[0,1,0x7FFFFFFF,0x80000000,0xFFFFFFFF]
    return [dict(seed=0x236000+i,old=old,target=target,condition=condition)for i,(old,target,condition)in enumerate((old,target,condition)for old in values for target in values for condition in [0,0x25,0xFFFFFFFF])]


def construct(recipe):
    rng=random.Random(recipe['seed'])
    state={WORD:bytearray(rng.randbytes(4)),OBJECT:bytearray(rng.randbytes(40)),CLEAR:bytearray(rng.randbytes(256)),CONTEXT:bytearray(rng.randbytes(16))}
    initial=[(a,bytes(b))for a,b in state.items()];services=[];natives=[]
    def snapshot():return[(a,bytes(b))for a,b in state.items()]
    def effect(items):
        for a,b in items:
            base=next(base for base,data in state.items()if base<=a and a+len(b)<=base+len(data))
            state[base][a-base:a-base+len(b)]=b
    def call(address,arguments,result=None,extra=()):
        effects=[(CONTEXT+12,rng.randbytes(4))]+list(extra)
        services.append(dict(address=address,arguments=arguments,result=rng.getrandbits(32)if result is None else result,effects=effects,before=snapshot()))
        effect(effects)
    def native(address,arguments,result,extra=()):
        natives.append(dict(address=address,arguments=arguments,result=result,before=snapshot()))
        effect(extra)
    call(0x020684AC,[3,0]);call(0x020684AC,[2,1])
    call(0x020642DC,[],recipe['condition'])
    if recipe['condition']==0x25:
        call(0x021DED5C,[15,4,77]);phase=12
    else:
        call(0x021DFF30,[],extra=[(CLEAR,rng.randbytes(256))])
        native(0x02063EEC,[],CLEAR)
        native(0x02008D78,[CLEAR,0,256],CLEAR+256,[(CLEAR,b'\0'*256)])
        call(0x021DED5C,[15,4,38]);call(0x021DEF28,[1])
        call(0x021DF590,[82],extra=[(WORD,struct.pack('<I',recipe['old'])),(OBJECT+36,struct.pack('<I',recipe['target']))])
        native(0x02063EE0,[],WORD);native(0x02067B58,[],OBJECT)
        if recipe['old']<recipe['target']:
            native(0x02063EE0,[],WORD);native(0x02067B58,[],OBJECT)
            effect([(WORD,struct.pack('<I',recipe['target']))])
            call(0x020684AC,[4,0],extra=[(WORD,rng.randbytes(4))])
            call(0x021DF974,[3,21,0x02217C18,0x1100]);phase=13
        else:
            call(0x021DF974,[3,23,0x02217BF0,16]);phase=0
    native(0x021E2F58,[phase],phase,[(CONTEXT+12,struct.pack('<I',phase))])
    return initial,snapshot(),services,natives,phase
