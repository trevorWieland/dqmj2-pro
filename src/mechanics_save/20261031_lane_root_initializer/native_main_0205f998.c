#include "root_initializer.h"
extern void native_fn_02008c14(u32,void *,u32);

void native_main_0205f998(u8 *buffer) {
    s8 index;
    u8 *destination;
    native_fn_02008c14(0,buffer,0x48);
    *(u32 *)buffer=127;
    buffer[8]=127;
    index=0;
    do {
        destination=buffer+index;
        destination[9]=127;
        index+=1;
    } while ((s32)index<4);
}
