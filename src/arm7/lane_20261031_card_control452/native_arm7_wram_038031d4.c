#include "native_card_frontier_types.h"
void native_arm7_wram_038031d4(u32 tag,u32 data,s32 enabled)
{
    if(tag==11 && enabled) {
        CardCommonStorage *state=&native_host_arm7_data_038090c0;
        if(CardReadPhase(state)==0) CardWriteRequest(state,data);
        switch(CardReadRequest(state)) {
            case 0: {
                u32 phase=CardReadPhase(state);
                if(phase!=0) {
                if(phase==1) {
                    state->prefix.argument=(CardArgument *)data;
                    state->flags|=0x10;
                }
                }
                break;
            }
            case 2: case 3: case 4: case 5: case 6: case 7: case 8:
            case 9: case 10: case 11: case 12: case 13: case 14: case 15:
                state->flags|=0x10;
                break;
            default: break;
        }
        if(!(state->flags&0x10)) state->prefix.command=CardReadPhase(state)+1;
        else {
            state->prefix.command=0;
            native_host_arm7_fn_037fc36c((state->flags&4)?state->prefix.currentThread:state->prefix.thread);
        }
    }
}
