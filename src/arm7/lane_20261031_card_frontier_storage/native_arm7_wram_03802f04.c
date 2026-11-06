#include "native_card_frontier_types.h"
void native_arm7_wram_03802f04(u32 value)
{
    if(!native_host_arm7_fn_03802824()) return;
    u8 command[2];
    CardArgument *argument=CARD_COMMON.argument;
    command[1]=(u8)value;
    command[0]=1;
    s32 retries=10;
    do {
        native_host_arm7_fn_038029d8();
        CARD_COMMAND.count=2;
        native_host_arm7_fn_03802860(command,0,2,native_host_arm7_fn_03802924);
        native_host_arm7_fn_0380272c(5,0);
        if(argument->result!=4) break;
        --retries;
    } while(retries>0);
}
