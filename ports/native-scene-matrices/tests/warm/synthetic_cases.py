import ctypes as C
from warm_api import *

def simple(mode=3):
    p=full43([4097,511,-7,-1024,6145,301,0,-2048,8193,17,-31,7])
    seed=dict(camera=full43([3851,613,-227,-701,4327,89,317,-449,3761,1023,-4097,813]),
        inverse=full43([3077,-193,41,311,4501,-79,-37,151,3907,-991,2059,-503]),
        srt=full43([4121,-199,73,257,3989,-131,43,229,4273,211,-193,313]),
        inverseSrt=full43([3907,149,-67,-113,4211,193,71,-257,4013,-433,607,-293]))
    return fixture(p,mode,seed)

def mutations():
    return [
        ('program',lambda o,c,s:setattr(o.model.scope,'program',1),-1),
        ('CPU',lambda o,c,s:setattr(o.model.scope,'processor',7),-1),
        ('module',lambda o,c,s:setattr(o.model.scope,'module',2),-1),
        ('mapping-generation',lambda o,c,s:setattr(o.model.scope,'generation',0),-1),
        ('model-address',lambda o,c,s:setattr(o.model,'model_set',0),-1),
        ('instance',lambda o,c,s:setattr(o,'instance_id',0),-1),
        ('run-generation',lambda o,c,s:setattr(o,'run_generation',0),-1),
        ('matrix-generation',lambda o,c,s:setattr(o,'matrix_generation',0),-1),
        ('projection-generation',lambda o,c,s:setattr(o,'projection_generation',0),-1),
        ('queue-generation',lambda o,c,s:setattr(o,'queue_generation',0),-1),
        ('stale-camera',lambda o,c,s:setattr(c.owner,'camera_generation',99),-1),
        ('stale-cache',lambda o,c,s:setattr(c.owner,'cache_generation',99),-1),
        ('zero-base-generation',lambda o,c,s:setattr(o,'base_generation',0),-1),
        ('raw-flush-bits',lambda o,c,s:setattr(c,'raw_flush_bits',4),-1),
        ('branch-precedence',lambda o,c,s:setattr(c,'branch',1),-1),
        ('cold-cache',lambda o,c,s:setattr(c,'selected_state',1),-2),
        ('missing-cache',lambda o,c,s:setattr(c,'selected_state',0),-2),
        ('missing-valid-mask',lambda o,c,s:setattr(c,'cache_valid_mask',0),-2),
        ('wrong-valid-mask',lambda o,c,s:setattr(c,'cache_valid_mask',8),-2),
        ('unknown-valid-mask',lambda o,c,s:setattr(c,'cache_valid_mask',0x81),-2),
        ('provider',lambda o,c,s:setattr(c,'provider_flags',1),-2),
        ('entry-mode',lambda o,c,s:setattr(s.matrix,'mode',0),-2),
        ('matrix-owner',lambda o,c,s:setattr(s.matrix.owner,'model_index',99),-1),
        ('slot31',lambda o,c,s:setattr(s.matrix,'valid_slots',1<<31),-1),
        ('projection-depth',lambda o,c,s:setattr(s,'projection_depth',1),-2),
        ('unknown-projection-error',lambda o,c,s:setattr(s,'projection_error_known',0),-2),
        ('projection-error',lambda o,c,s:setattr(s,'projection_error',1),-2),
        ('saved-valid-encoding',lambda o,c,s:setattr(s,'projection_saved_valid',2),-1),
        ('incomplete-queue',lambda o,c,s:setattr(s,'queue_complete',0),-2),
        ('nonempty-queue',lambda o,c,s:setattr(s,'queued_commands',1),-2),
        ('unknown-async',lambda o,c,s:setattr(s,'async_known',0),-2),
        ('active-async',lambda o,c,s:setattr(s,'async_active',1),-2)]

def pointers(fn):
    names=[]
    for missing in range(5):
        owner,context,entry=simple();out=State();effect=Effect()
        C.memset(C.byref(out),0xa5,C.sizeof(out));C.memset(C.byref(effect),0x5a,C.sizeof(effect))
        values=[owner,context,entry,out,effect];before=[bytes(v) for v in values];args=[C.byref(v) for v in values];args[missing]=None
        assert fn(*args)==-1 and [bytes(v) for v in values]==before
        names.append('null-'+str(missing))
    for kind in ['output-is-entry','effect-is-context','outputs-overlap','unaligned-output','wrapping-output']:
        owner,context,entry=simple();out=State();effect=Effect();large=C.create_string_buffer(6000)
        values=[owner,context,entry,out,effect,large];before=[bytes(v) for v in values]
        args=[C.byref(v) for v in values[:5]]
        if kind=='output-is-entry':args[3]=C.byref(entry)
        if kind=='effect-is-context':args[4]=C.cast(C.byref(context),C.POINTER(Effect))
        if kind=='outputs-overlap':args[4]=C.cast(C.addressof(out)+4000,C.POINTER(Effect))
        if kind=='unaligned-output':args[3]=C.cast(C.addressof(large)+1,C.POINTER(State))
        if kind=='wrapping-output':args[3]=C.cast(C.c_void_p(2**(C.sizeof(C.c_void_p)*8)-4),C.POINTER(State))
        assert fn(*args)==-1 and [bytes(v) for v in values]==before,kind
        names.append(kind)
    return names

def check_synthetic(fn):
    positive=[]
    for mode in range(4):
        owner,context,entry=simple(mode)
        invoke(fn,owner,context,entry);positive.append('general-stored-'+str(mode))
    owner,context,entry=simple(0)
    for name in ['camera_id','camera_generation','base_generation','cache_generation']:
        setattr(owner,name,0);setattr(context.owner,name,0);setattr(entry.owner,name,0)
    context.forward43[:]=[-2**31]*12;context.stored_inverse43[:]=[2**31-1]*12
    invoke(fn,owner,context,entry);positive.append('NONE-no-camera-no-hidden-array-read')
    owner,context,entry=simple();entry.projection_saved_valid=1
    invoke(fn,owner,context,entry);positive.append('existing-projection-saved-slot-overwritten')
    owner,context,entry=simple(0);entry.matrix.matrices[1][0:3]=[1,1,1]
    invoke(fn,owner,context,entry);positive.append('rounded-small-norm')
    negative=[]
    for name,change,status in mutations():
        owner,context,entry=simple();change(owner,context,entry);invoke(fn,owner,context,entry,status)
        negative.append(dict(name=name,status=status))
    return dict(positive=positive,refusals=negative,pointerRefusals=pointers(fn))
