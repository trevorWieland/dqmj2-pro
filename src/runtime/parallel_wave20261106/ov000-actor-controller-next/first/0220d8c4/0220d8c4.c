#include "context.h"
u32 native_ov000_0220d8c4(ActorView *actor)
{
    u32 result=0;
    if(actor->phase==0){
        native_fn_ov000_0220ce54(actor);
        actor->timer=(s16)((native_fn_0203d294(2147483647)&31)+30);
        actor->phase=10;
    }
    if(actor->phase==10){
        actor->timer=(s16)(actor->timer-1);
        if(actor->timer<=0)actor->phase=20;
    }
    if(actor->phase==20){
        native_fn_ov000_0220a2a4(actor,0,0);
        actor->phase=30;
        actor->timer=0;
    }
    if(actor->phase==30){
        actor->timer=(s16)(actor->timer+1);
        if(actor->timer>15){actor->timer=0;actor->phase=40;}
    }
    if(actor->phase==40){
        native_fn_02042104(actor,368640,0);
        actor->timer=(s16)(actor->timer+1);
        if(actor->timer>=2)actor->phase=100;
    }
    if(actor->phase==100){native_fn_ov000_02209c68(actor,3);result=1;}
    return result;
}
