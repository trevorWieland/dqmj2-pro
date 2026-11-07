#include "context.h"
u32 native_ov000_02210008(ActorView *actor)
{
    u32 result=1;
    u8 state=actor->state;
    if(state==9)result=0;
    else if(state==1)result=0;
    else if(state==7)result=0;
    else{
        if(state==3&&native_fn_020c56b4(actor->id)->unknown5[2]==8)result=0;
        else if(actor->state==6&&native_fn_020c56b4(actor->id)->unknown5[3]==3)result=0;
    }
    return result;
}
