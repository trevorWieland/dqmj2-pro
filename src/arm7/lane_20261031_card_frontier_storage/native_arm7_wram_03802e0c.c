#include "native_card_frontier_types.h"
void native_arm7_wram_03802e0c(u32 address,u32 length)
{
    CardExtendedArgument *argument=(CardExtendedArgument *)CARD_COMMON.argument;
    u32 size=argument->prefix.unknown20;
    if((address|length)&(size-1)) { argument->prefix.result=2; return; }
    if(!native_host_arm7_fn_03802824()) return;
    while(length!=0) {
        native_host_arm7_fn_038029d8();
        CARD_COMMAND.count=argument->prefix.addressWidth+1;
        native_host_arm7_fn_03802a0c(address,0x20);
        native_host_arm7_fn_0380272c(argument->field48,argument->field4c);
        if(argument->prefix.result!=0) return;
        address+=size;
        length-=size;
    }
}
