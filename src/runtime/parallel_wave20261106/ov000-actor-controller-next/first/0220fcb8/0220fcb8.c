#include "context.h"
u32 native_ov000_0220fcb8(ActorView *actor)
{
    u32 result=0;
    u8 state=actor->state;
    if(state!=9&&state!=4){
        if(native_fn_020c56b4(actor->id)->unknown5[5]!=7){
            u8 kind=native_fn_020c56b4(actor->id)->unknown5[2];
            if(kind==6&&actor->state==3)native_fn_ov000_02209c68(actor,4);
            else native_fn_ov000_02209c68(actor,9);
            result=1;
        }
    }
    return result;
}
