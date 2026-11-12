#include "context.h"
u32 native_ov000_0220cd28(ActorView *actor)
{
    if(actor->phase==0){
        native_fn_ov000_0220a2a4(actor,0,0);
        actor->timer=1;
        actor->phase=10;
        if(!native_fn_ov000_0220cbe0(actor))native_fn_ov000_02209c68(actor,6);
    }
    if(actor->phase==10){
        s32 target=native_fn_02028158(native_fn_0202818c(&actor->position,ov000_saved_world_position_get_021e07b8(0)));
        s32 difference=native_fn_02028158((s32)((u32)target-native_fn_02042c2c(actor)));
        if(difference < -8192||difference>8192){
            if(difference>0)native_fn_02042104(actor,8192,0);
            else native_fn_02042104(actor,-8192,0);
        }else native_fn_02041f90(actor,target,0);
        actor->timer=(s16)(actor->timer+1);
        if(actor->timer>60){
            if(native_fn_ov000_0220aac4(actor,0))actor->timer=0;
            else native_fn_ov000_02209c68(actor,7);
        }
    }
    return 0;
}
