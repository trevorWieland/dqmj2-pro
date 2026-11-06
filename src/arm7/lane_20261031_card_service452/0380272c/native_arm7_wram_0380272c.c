#include "native_card_service_types.h"
void native_arm7_wram_0380272c(u32 minimum,u32 maximum)
{
    if(minimum+maximum==0) return;
    if(minimum!=0) native_host_arm7_fn_037fc468((s32)minimum);
    if(maximum!=0) {
        s32 remaining=(s32)(maximum-minimum);
        while(!CardStatusReady() && remaining>0) {
            s32 interval=remaining<5?remaining:5;
            native_host_arm7_fn_037fc468(interval);
            remaining-=interval;
        }
    }
    if(!CardStatusReady()) CARD_COMMON.argument->result=4;
}
