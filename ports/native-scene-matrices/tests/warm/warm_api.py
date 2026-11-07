import ctypes as C
import math


U=C.c_uint32
I=C.c_int32
M=I*16


class Scope(C.Structure):
    _fields_=[(n,U) for n in ['program','processor','module','generation']]


class MatrixOwner(C.Structure):
    _fields_=[('scope',Scope),('model_set',U),('model_index',U)]


class MatrixState(C.Structure):
    _fields_=[('owner',MatrixOwner),('mode',U),('valid_slots',U),('matrices',M*4),('position_stack',M*32),('vector_stack',M*32)]


class Command(C.Structure):
    _fields_=[('owner',MatrixOwner),('opcode',U),('count',U),('arguments',M)]


class Owner(C.Structure):
    _fields_=[('model',MatrixOwner)]+[(n,U) for n in ['instance_id','run_generation','matrix_generation','camera_id',
        'camera_generation','base_generation','cache_generation','projection_generation','queue_generation']]


class Context(C.Structure):
    _fields_=[('owner',Owner)]+[(n,U) for n in ['raw_flush_bits','branch','selected_state','cache_valid_mask','provider_flags']]+[('forward43',I*12),('stored_inverse43',I*12)]


class State(C.Structure):
    _fields_=[('owner',Owner),('matrix',MatrixState)]+[(n,U) for n in ['projection_depth','projection_error_known','projection_error',
        'projection_saved_valid']]+[('projection_saved',M)]+[(n,U) for n in ['queue_complete','queued_commands','async_known','async_active']]


class Effect(C.Structure):
    _fields_=[('owner',Owner)]+[(n,U) for n in ['raw_flush_bits','branch','cache_valid_mask','logical_commands','terminal_count',
        'source_effect_count','projection_depth_before','projection_depth_after','projection_slot_written']]+[
        ('readback',M),('corrected',M),('translation',I*3),('magnitudes',I*3),('saved_projection',M),('source_operations',U*9),('terminal',Command*4)]


assert [C.sizeof(t) for t in [Scope,MatrixOwner,MatrixState,Command,Owner,Context,State,Effect]]==[16,24,4384,96,60,176,4540,732]


def identity():
    return [4096 if i%5==0 else 0 for i in range(16)]


def full43(a):
    out=identity()
    for r in range(4):out[r*4:r*4+3]=a[r*3:r*3+3]
    return out


def as43(a):
    return [a[r*4+c] for r in range(4) for c in range(3)]


def multiply(a,b):
    out=[]
    for r in range(4):
        for c in range(4):
            terms=[a[r*4+k]*b[k*4+c] for k in range(4)]
            if sum(abs(v) for v in terms)>2**63-1:raise ArithmeticError('absolute-sum')
            value=sum(terms)//4096
            if not -2**31<=value<2**31:raise ArithmeticError('dot-narrow')
            out.append(value)
    return out


def fixture(p,mode,seed,number=1,before=None,warm=True,mask=None):
    owner=Owner();owner.model.scope=Scope(0,9,1,7);owner.model.model_set=0x02700000;owner.model.model_index=2
    for n,t in Owner._fields_[1:]:setattr(owner,n,number+11)
    context=Context();context.owner=owner;context.raw_flush_bits=mode;context.branch=2 if mode&1 else 1 if mode&2 else 0
    context.selected_state=(2 if warm else 1) if mode else 0
    context.cache_valid_mask=(0x80 if mode&1 else 8 if mode&2 else 0) if mask is None else mask
    forward=seed['srt'] if mode&1 else seed['camera'];inverse=seed['inverseSrt'] if mode&1 else seed['inverse']
    context.forward43[:]=as43(forward);context.stored_inverse43[:]=as43(inverse)
    entry=State();entry.owner=owner;entry.matrix.owner=owner.model;entry.matrix.mode=2
    q=identity();q[0]=8192;q[5]=3072;q[12]=31
    v=identity();v[1]=1024;v[12]=19
    tex=identity();tex[5]=8192;tex[13]=-7
    for i,a in enumerate(before['matrices'] if before else [q,p,v,tex]):entry.matrix.matrices[i][:]=a
    if before:
        for i,slot in enumerate(before['positionSlots']):
            entry.matrix.position_stack[i][:]=slot[0];entry.matrix.vector_stack[i][:]=slot[1]
        entry.projection_saved[:]=before['projectionSlot']
    else:
        entry.matrix.valid_slots=1<<4
        entry.matrix.position_stack[4][:]=[37+i*11 for i in range(16)]
        entry.matrix.vector_stack[4][:]=[-73+i*3 for i in range(16)]
        entry.projection_saved[:]=[-13+i*7 for i in range(16)]
    entry.projection_error_known=entry.queue_complete=entry.async_known=1
    return owner,context,entry


def reference(owner,context,entry):
    result=State.from_buffer_copy(bytes(entry));effect=Effect();effect.owner=owner
    effect.raw_flush_bits=context.raw_flush_bits;effect.branch=context.branch;effect.cache_valid_mask=context.cache_valid_mask
    p=list(entry.matrix.matrices[1]);m=multiply(p,full43(list(context.forward43))) if context.branch else p[:]
    scales=[]
    for at in [0,4,8]:
        total=sum(v*v for v in m[at:at+3])
        if total>2**60-2**30:raise ArithmeticError('norm-domain')
        scales.append((math.isqrt(total*4)+1)//2)
    t=identity();t[12:15]=m[12:15]
    inverse=full43(list(context.stored_inverse43))
    vector=multiply(t,inverse) if context.branch else t[:]
    position=vector[:]
    for r in range(3):
        for c in range(4):
            value=vector[r*4+c]*scales[r]//4096
            if not -2**31<=value<2**31:raise ArithmeticError('scale-narrow')
            position[r*4+c]=value
    result.matrix.matrices[1][:]=position;result.matrix.matrices[2][:]=vector
    result.projection_saved[:]=entry.matrix.matrices[0];result.projection_saved_valid=1
    effect.readback[:]=p;effect.corrected[:]=m;effect.translation[:]=m[12:15];effect.magnitudes[:]=scales
    effect.saved_projection[:]=entry.matrix.matrices[0];effect.projection_slot_written=1
    operations=[0x10,0x11,0x15,0x10000,0x12,0x10,0x17]+([0x19] if context.branch else [])+[0x1b]
    effect.source_effect_count=len(operations);effect.source_operations[:len(operations)]=operations
    commands=[(0x10,[2]),(0x17,list(context.stored_inverse43) if context.branch else as43(t))]
    if context.branch:commands.append((0x19,as43(t)))
    commands.append((0x1b,scales));effect.terminal_count=len(commands);effect.logical_commands=len(operations)-1
    for i,(op,args) in enumerate(commands):
        effect.terminal[i].owner=owner.model;effect.terminal[i].opcode=op;effect.terminal[i].count=len(args)
        effect.terminal[i].arguments[:len(args)]=args
    return result,effect


def function(path):
    library=C.CDLL(str(path));fn=library.j2p_billboard_warm
    fn.argtypes=[C.POINTER(Owner),C.POINTER(Context),C.POINTER(State),C.POINTER(State),C.POINTER(Effect)]
    fn.restype=C.c_int
    return fn


def invoke(fn,owner,context,entry,expected_status=1,expected=None):
    output=State();effect=Effect();C.memset(C.byref(output),0xa5,C.sizeof(output));C.memset(C.byref(effect),0x5a,C.sizeof(effect))
    original=[bytes(v) for v in [owner,context,entry]];unchanged=[bytes(output),bytes(effect)]
    status=fn(C.byref(owner),C.byref(context),C.byref(entry),C.byref(output),C.byref(effect))
    assert status==expected_status,(status,expected_status)
    assert [bytes(v) for v in [owner,context,entry]]==original
    if status==1:
        wanted=reference(owner,context,entry) if expected is None else expected
        assert bytes(output)==bytes(wanted[0]),'state mismatch'
        assert bytes(effect)==bytes(wanted[1]),'effect mismatch'
    else:assert [bytes(output),bytes(effect)]==unchanged,'partial output on refusal'
    return output,effect
