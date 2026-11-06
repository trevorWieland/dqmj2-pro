#include "native_card_frontier_types.h"
void native_arm7_wram_03803114(CardCommonStorage *state,void (*callback)(void *),void *argument)
{
    u32 mode=native_host_arm7_fn_037fdd00();
    while(state->flags&4) native_host_arm7_fn_037fc290(state->prefix.busyQueue);
    state->flags|=4;
    state->prefix.callback=callback;
    state->prefix.callbackArgument=argument;
    native_host_arm7_fn_037fdd14(mode);
}
