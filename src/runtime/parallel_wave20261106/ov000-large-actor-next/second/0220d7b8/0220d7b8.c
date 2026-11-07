#include "context.h"
u32 native_ov000_0220d7b8(ActorView *actor)
{
    u32 result=1;
    u8 phase=actor->phase;
    if(phase==0){
        if(native_fn_ov000_0220aac4(actor,0)){
            actor->timer=(s16)(native_fn_0203d294(60)+30);
            native_fn_ov000_0220a2a4(actor,2,0);
            native_fn_02042bfc(actor,native_fn_020c56b4(actor->id)->word18);
            actor->phase=10;
        }else{
            if(native_fn_020c56b4(actor->id)->unknown5[2]==6)native_fn_ov000_02209c68(actor,7);
            else native_fn_ov000_02209c68(actor,3);
            result=0;
        }
    }else if(phase==10){
        if(!(actor->timer&2))native_fn_02042104(actor,(s32)native_fn_ov000_0220c598((s32)actor)>>2,0);
        actor->timer=(s16)(actor->timer-1);
        if(actor->timer<=0)actor->phase=0;
    }
    return result;
}
