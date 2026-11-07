#include "context.h"
u32 native_ov000_0220c768(ActorView *actor)
{
    u32 result=0;
    s16 timer;
    Vec3 collision;
    if(actor->timer==0){
        actor->anchorY=actor->position.y;
        actor->thresholdY=(s32)((u32)actor->position.y-20480u);
        actor->flag2c1=1;
        native_fn_02042c0c(actor,31);
        native_fn_ov000_0221089c(actor,1);
    }
    timer=actor->timer;
    actor->position.y=(s32)((u32)actor->anchorY-(u32)((s32)((u32)timer*(u32)(timer*178))>>1));
    if(native_fn_ov000_021dc374(&actor->position,actor->collision,&collision,native_fn_020c56b4(actor->id)->unknown5[7])){
        actor->position.y=collision.y;
        actor->flag2c1=0;
        result=1;
    }
    actor->timer=(s16)(actor->timer+1);
    return result;
}
