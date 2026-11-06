#include "native_card_frontier_types.h"
void native_arm7_wram_03802ffc(void)
{
    CardTaskState *state=(CardTaskState *)&CARD_COMMON;
    state->prefix.argument->result=0;
    u32 interrupts;
    void *argument;
    void (*callback)(void *);
    callback=state->prefix.callback;
    argument=state->prefix.callbackArgument;
    interrupts=native_host_arm7_fn_037fdd00();
    state->flags&=~0x4c;
    native_host_arm7_fn_037fc2e4(state->prefix.busyQueue);
    if(state->flags&0x10) native_host_arm7_fn_037fc36c(state->prefix.thread);
    native_host_arm7_fn_037fdd14(interrupts);
    if(callback) callback(argument);
}
