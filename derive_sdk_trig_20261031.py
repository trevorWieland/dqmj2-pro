from decimal import Decimal,localcontext,ROUND_HALF_EVEN
from pathlib import Path


def arctangent_inverse(denominator):
    x=Decimal(1)/denominator
    square=x*x
    power=x
    total=Decimal(0)
    index=0
    while True:
        term=power/(2*index+1)
        if abs(term)<Decimal('1e-105'):
            break
        total+=term if index%2==0 else -term
        power*=square
        index+=1
    return total


def derive():
    with localcontext() as context:
        context.prec=110
        pi=16*arctangent_inverse(5)-4*arctangent_inverse(239)
        quarter=[]
        margin=Decimal(1)
        for index in range(1025):
            angle=pi*index/2048
            term=angle
            total=term
            order=1
            while abs(term)>Decimal('1e-100'):
                term*=-(angle*angle)/((2*order)*(2*order+1))
                total+=term
                order+=1
            scaled=4096*total
            rounded=scaled.to_integral_value(rounding=ROUND_HALF_EVEN)
            quarter.append(int(rounded))
            margin=min(margin,Decimal('0.5')-abs(scaled-rounded))
        sine=[]
        for phase in range(4096):
            quadrant,index=divmod(phase,1024)
            value=quarter[index] if quadrant%2==0 else quarter[1024-index]
            sine.append(value if quadrant<2 else -value)
        pairs=[(sine[phase],sine[(phase+1024)%4096]) for phase in range(4096)]
        return pairs,{'phaseCount':4096,'fixedPointScale':4096,'storage':'4096 interleaved signed16 sine/cosine pairs',
            'piDerivation':'16 atan(1/5) - 4 atan(1/239), alternating series',
            'decimalPrecision':110,'arctangentTermThreshold':'1e-105','sineTermThreshold':'1e-100',
            'rounding':'nearest, half even','minimumDistanceFromRoundingBoundary':str(margin),
            'originalInputBytesRead':0,'quarterWaveSymmetry':True}


def source_text(pairs):
    lines=['typedef signed short fx16;','const fx16 native_math_sincos_020d3fe0[8192] = {']
    for offset in range(0,len(pairs),16):
        lines.append('    '+', '.join(str(value) for pair in pairs[offset:offset+16] for value in pair)+',')
    lines.append('};')
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    from project import ROOT,write_json,sha256
    pairs,metadata=derive()
    path=ROOT/'generated/math/20261031_sincos_data.c'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(source_text(pairs),encoding='utf-8')
    write_json(ROOT/'evidence/attempts/sdk-trig-mathematical-source-20261031.json',{'sourceCredit':0,'derivation':metadata,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'physicalLines':len(path.read_text().splitlines())})
    print({'pairs':len(pairs),'minimumRoundingMargin':metadata['minimumDistanceFromRoundingBoundary'],'sourceLines':len(path.read_text().splitlines())})
