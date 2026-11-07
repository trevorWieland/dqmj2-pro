#include "context.h"
u32 native_ov000_0220ed9c(ActorView *actor)
{
    u32 result=0;
    if(actor->phase==0){
        s32 angle;
        native_fn_ov000_0220a2a4(actor,1,0);
        angle=(s32)native_fn_0203d294(90)-45;
        angle+=180;
        angle=(s32)((u32)angle<<12);
        actor->turn=native_fn_02028158(angle)>>5;
        actor->timer=0;
        actor->phase=10;
    }
    if(actor->phase==10){
        native_fn_02042104(actor,actor->turn,0);
        actor->timer=(s16)(actor->timer+1);
        if(actor->timer>32)actor->phase=20;
    }
    if(actor->phase==20){
        native_fn_ov000_0220a2a4(actor,1,0);
        actor->timer=(s16)((native_fn_0203d294(2147483647)&63)+60);
        actor->phase=30;
    }
    if(actor->phase==30){
        if(!(actor->timer&3)&&native_fn_ov000_0220aac4(actor,1))actor->phase=200;
        actor->timer=(s16)(actor->timer-1);
        if(actor->timer<=0)actor->phase=100;
    }
    if(actor->phase==100){native_fn_ov000_02209c68(actor,3);result=1;}
    else if(actor->phase==200){
        if(native_fn_020c56b4(actor->id)->unknown5[2]==6)native_fn_ov000_02209c68(actor,5);
        else native_fn_ov000_02209c68(actor,4);
        result=1;
    }
    return result;
}
