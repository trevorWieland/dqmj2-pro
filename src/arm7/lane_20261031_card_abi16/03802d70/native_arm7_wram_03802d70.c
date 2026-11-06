#include "native_card_service_types.h"
void native_arm7_wram_03802d70(u32 address,u32 length)
{
    CardArgument *argument=CARD_COMMON.argument;
    u32 size=argument->sectorSize;
    if((address|length)&(size-1)) { argument->result=2; return; }
    if(!native_host_arm7_fn_03802824()) return;
    while(length!=0) {
        native_host_arm7_fn_038029d8();
        CARD_COMMAND.count=argument->addressWidth+1;
        native_host_arm7_fn_03802a0c(address,0xd8);
        native_host_arm7_fn_0380272c(argument->eraseDelay,argument->eraseTotal);
        if(argument->result!=0) return;
        address+=size;
        length-=size;
    }
}
