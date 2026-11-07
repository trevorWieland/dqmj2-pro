from warm_api import *


def numeric_cases(fn):
    b=2**31-1;records=[]
    for name,stage,amount,status in [
        ('norm-safe','norm',255,1),('norm-refuse','norm',256,-4),
        ('absolute-safe','absolute',4,1),('absolute-refuse','absolute',5,-4),
        ('CPU-narrow-safe','CPU',4096,1),('CPU-narrow-refuse','CPU',4097,-4),
        ('GPU-dot-safe','GPU-dot',4096,1),('GPU-dot-refuse','GPU-dot',4097,-4),
        ('GPU-scale-safe','GPU-scale',8192,1),('GPU-scale-refuse','GPU-scale',8193,-4)]:
        owner,context,entry=__import__('synthetic_cases').simple(0 if stage=='norm' else 2)
        context.forward43[:]=as43(identity());context.stored_inverse43[:]=as43(identity())
        p=identity()
        if stage=='norm':p[0:3]=[2**30-1,32767,amount]
        if stage=='absolute':
            p=[0]*16;p[0:3]=[b,b,amount];p[15]=4096
            context.forward43[:]=[b,0,0,-b,0,0,b,0,0,0,0,0]
        if stage=='CPU':
            p=[0]*16;p[12]=amount;p[15]=4096;context.forward43[0]=b
        if stage=='GPU-dot':p[12]=b;context.stored_inverse43[0]=amount
        if stage=='GPU-scale':p[0]=2**30-1;context.stored_inverse43[0]=amount
        entry.matrix.matrices[1][:]=p
        invoke(fn,owner,context,entry,status);records.append(dict(name=name,status=status))
    return records
