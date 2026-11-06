#include "native_card_service_types.h"
void native_arm7_wram_03802624(void)
{
    CardCommon *state=&CARD_COMMON;
    state->owner=-3;
    state->priority=4;
    state->references=0;
    state->target=0;
    state->argument=0;
    state->command=0;
    state->lockQueue[1]=0;
    state->lockQueue[0]=0;
    state->busyQueue[1]=0;
    state->busyQueue[0]=0;
    native_host_arm7_fn_037fc054(state->thread,native_host_arm7_fn_038032b8,0,
        &native_host_arm7_data_038096c0,1024,state->priority);
    native_host_arm7_fn_037fc36c(state->thread);
    native_host_arm7_fn_037fe39c(11,native_host_arm7_fn_038031d4);
    if(CardIsChild()) return;
    native_host_arm7_data_038090a0=1;
}
