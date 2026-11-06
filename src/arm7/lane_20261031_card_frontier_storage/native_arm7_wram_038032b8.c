#include "native_card_frontier_types.h"
void native_arm7_wram_038032b8(void *unused)
{
    (void)unused;
    CardTaskState *state=(CardTaskState *)&CARD_COMMON;
    for(;;) {
        s32 received=0;
        u32 interrupts=native_host_arm7_fn_037fdd00();
        for(;;) {
            if(!(state->flags&4)) {
                if(state->flags&0x10) {
                    received=1;
                    state->flags|=4;
                    state->flags&=~0x10;
                    break;
                }
            } else if(state->flags&8) break;
            state->prefix.currentThread=state->prefix.thread;
            native_host_arm7_fn_037fc290(0);
        }
        native_host_arm7_fn_037fdd14(interrupts);
        if(received) {
            state->prefix.argument->result=0;
            CardDispatchArgument *argument=(CardDispatchArgument *)state->prefix.argument;
            u32 request=state->prefix.unknown04;
            if(!(argument->caps&(1U<<request))) argument->prefix.result=3;
            else switch(request) {
                case 0: case 1: break;
                case 2: native_host_arm7_fn_03802aac(); break;
                case 3: state->prefix.argument->id=native_host_arm7_fn_03803094(); break;
                case 4: argument->prefix.result=3; break;
                case 6: native_host_arm7_fn_03802b04(argument->prefix.src,argument->prefix.dst,argument->prefix.length); break;
                case 7: native_host_arm7_fn_03802c28(argument->prefix.dst,(const void *)argument->prefix.src,argument->prefix.length); break;
                case 8: native_host_arm7_fn_03802b70(argument->prefix.dst,(const void *)argument->prefix.src,argument->prefix.length); break;
                case 9: native_host_arm7_fn_03802ce0(argument->prefix.dst,(const void *)argument->prefix.src,argument->prefix.length); break;
                case 11: native_host_arm7_fn_03802d70(argument->prefix.dst,argument->prefix.length); break;
                case 15: native_host_arm7_fn_03802e0c(argument->prefix.dst,argument->prefix.length); break;
                case 12: native_host_arm7_fn_03802ea8(); break;
                case 13: *(u8 *)state->prefix.argument->dst=native_host_arm7_fn_038027d0(); break;
                case 14: native_host_arm7_fn_03802f04(*(u8 *)argument->prefix.src); break;
                default: argument->prefix.result=3; break;
            }
            while(native_host_arm7_fn_037fe410(11,1,1)<0) {}
            u32 mode=native_host_arm7_fn_037fdd00();
            state->flags&=~0x4c;
            native_host_arm7_fn_037fc2e4(state->prefix.busyQueue);
            if(state->flags&0x10) native_host_arm7_fn_037fc36c(state->prefix.thread);
            native_host_arm7_fn_037fdd14(mode);
        } else state->prefix.task(state);
    }
}
