#include "context.h"
u32 native_main_02043570(void) {
    s32 i;
    s32 j;
    u32 result=0;
    Slot *slot;
    i=0;
    do {
        slot=native_fn_020649c0(i);
        if(slot->kind2e>=0) {
            j=0;
            do {
                slot->bytes0c[j]=native_fn_0203d294(249)+7;
                j++;
            }while(j<3);
            native_fn_02044ff4(slot->tailb6,slot->kind2e,slot->value30);
            result++;
        }
        i++;
    }while(i<3);
    return result;
}
