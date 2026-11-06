from decimal import Decimal,localcontext,ROUND_HALF_EVEN
from derive_sdk_trig_20261031 import arctangent_inverse


def derive():
    with localcontext() as context:
        context.prec=110
        pi=16*arctangent_inverse(5)-4*arctangent_inverse(239)
        result=[];margin=Decimal(1)
        for index in range(129):
            value=Decimal(index)/128;offset=Decimal(0)
            if value>Decimal('0.5'):
                value=(value-1)/(value+1);offset=pi/4
            power=value;total=offset;square=value*value;order=0
            while abs(power/(2*order+1))>=Decimal('1e-105'):
                term=power/(2*order+1);total+=term if order%2==0 else -term
                power*=square;order+=1
            scaled=total*4096;rounded=scaled.to_integral_value(rounding=ROUND_HALF_EVEN)
            result.append(int(rounded));margin=min(margin,Decimal('0.5')-abs(scaled-rounded))
        return result,{'originalInputBytesRead':0,'elements':129,'scale':4096,'decimalPrecision':110,'rounding':'nearest, half even','formula':'4096 atan(i/128)','minimumRoundingMargin':str(margin),'dataByteCredit':0}
