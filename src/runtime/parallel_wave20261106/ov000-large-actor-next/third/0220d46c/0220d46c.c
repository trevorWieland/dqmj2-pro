#include "context.h"
u32 native_ov000_0220d46c(ActorView *actor)
{
    u32 result=0;
    Vec3 destination;
    if(actor->phase==0){
        if(!native_fn_ov000_0220cbe0(actor))native_fn_ov000_02209c68(actor,6);
        else{
            native_fn_ov000_0220ce54(actor);
            actor->timer=(s16)((native_fn_0203d294(2147483647)&31)+60);
            actor->phase=10;
        }
    }
    if(actor->phase==10){
        actor->timer=(s16)(actor->timer-1);
        if(actor->timer<=0){
            native_fn_ov000_0220a2a4(actor,0,0);
            native_fn_02042104(actor,737280,0);
            if(native_fn_020c56b4(actor->id)->unknown5[2]==6)native_fn_ov000_02209c68(actor,7);
            else native_fn_ov000_02209c68(actor,3);
            result=1;
        }
        if(actor->flags2c2.high==1){
            s32 index=native_fn_ov000_0220e0d8(actor);
            if(index>=0){actor->scratch.index=(u8)index;actor->phase=50;}
        }
    }
    if(actor->phase==50){native_fn_ov000_0220a2a4(actor,0,0);actor->timer=0;actor->phase=52;}
    if(actor->phase==52){
        s32 remaining=31-actor->timer;
        if(remaining<=0)actor->phase=54;
        else{native_fn_02042c0c(actor,(u8)remaining);actor->timer=(s16)(actor->timer+2);}
        actor->flags2c2.low=remaining<20;
    }
    if(actor->phase==54){
        native_fn_ov000_021e60a8(actor->scratch.index,&destination);
        actor->position=destination;
        actor->secondaryPosition=destination;
        native_fn_020420c4(actor,native_fn_ov000_021e07b8(0));
        actor->timer=0;
        actor->phase=56;
    }
    if(actor->phase==56){
        s16 timer=actor->timer;
        native_fn_02042c0c(actor,(u8)timer);
        if(timer>=31)actor->phase=58;
        else actor->timer=(s16)(actor->timer+2);
        actor->flags2c2.low=timer<20;
    }
    if(actor->phase==58){
        native_fn_ov000_0220a2a4(actor,2,0);
        actor->phase=0;
        if(native_fn_020c56b4(actor->id)->unknown5[2]==6)native_fn_ov000_02209c68(actor,7);
        else native_fn_ov000_02209c68(actor,3);
        result=1;
    }
    return result;
}
