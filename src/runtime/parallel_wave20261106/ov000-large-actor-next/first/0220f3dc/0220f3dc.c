#include "context.h"
u32 native_ov000_0220f3dc(ActorView *actor)
{
    u32 result=0;
    if(!actor->flag1e2||!actor->active)actor->phase=30;
    if(actor->phase==0){
        native_fn_ov000_0220a2a4(actor,2,0);
        native_fn_02042bfc(actor,native_fn_020c56b4(actor->id)->word18);
        actor->flags2c2=(u8)((actor->flags2c2&~15)|1);
        actor->phase=10;
    }
    if(actor->phase==10){
        actor->timer=(s16)(actor->timer+1);
        if(actor->timer<60){
            if(actor->timer%30==0){
                s32 angle=(s32)((180u*(native_fn_0203d294(2)+1)+90u)<<12);
                actor->turn=native_fn_02028158(angle)/30;
            }
            {
                u32 angle=native_fn_02042c2c(actor);
                angle+=(u32)actor->turn;
                native_fn_02041f90(actor,native_fn_02028158((s32)angle),0);
            }
        }else{actor->timer=31;actor->phase=20;}
    }
    if(actor->phase==20){
        actor->timer=(s16)(actor->timer-1);
        if(actor->timer<=0){native_fn_ov000_0220f018(actor);actor->flag1e2=0;actor->phase=30;result=1;}
        native_fn_02042c0c(actor,(u8)actor->timer);
        native_fn_ov000_0221089c(actor,0);
    }
    if(actor->phase==30){actor->flag1e2=0;actor->flags2c2&=~15;result=1;}
    return result;
}
