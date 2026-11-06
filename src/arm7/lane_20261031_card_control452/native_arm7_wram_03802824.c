#include "native_card_frontier_types.h"
s32 native_arm7_wram_03802824(void)
{
    native_host_arm7_fn_0380272c(0,50);
    CardArgument *argument=CARD_COMMON.argument;
    if(argument->result==4) { argument->result=6; return 0; }
    return 1;
}
