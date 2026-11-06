#include "native_card_service_types.h"
void native_arm7_wram_03802b70(u32 address,const u8 *source,u32 length)
{
    if(!native_host_arm7_fn_03802824()) return;
    u32 mask;
    CardArgument *argument=CARD_COMMON.argument;
    u32 size=argument->pageSize;
    mask=size-1;
    while(length!=0) {
        u32 chunk=size-(address&mask);
        if(chunk>length) chunk=length;
        native_host_arm7_fn_038029d8();
        CARD_COMMAND.count=argument->addressWidth+1+chunk;
        native_host_arm7_fn_03802a0c(address,2);
        native_host_arm7_fn_03802860(source,0,chunk,native_host_arm7_fn_03802924);
        native_host_arm7_fn_0380272c(argument->programDelay,0);
        if(argument->result!=0) return;
        source+=chunk;
        address+=chunk;
        length-=chunk;
    }
}
