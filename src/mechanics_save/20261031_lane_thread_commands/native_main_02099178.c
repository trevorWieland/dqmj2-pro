#include "thread_commands.h"
extern u32 native_fn_020068c0(void *thread);
extern void native_fn_020065f0(void *thread,void (*entry)(void *),void *argument,void *stack,u32 extent,u32 priority);
extern void native_fn_0200698c(void *thread);
extern void native_fn_020991d0(void *argument);
extern u8 *native_data_021d1914;

void native_main_02099178(void) {
    if (*(u32 *)(native_data_021d1914+0x1188)==0 || native_fn_020068c0(native_data_021d1914+0x111C)!=0) {
        native_fn_020065f0(native_data_021d1914+0x111C,native_fn_020991d0,native_data_021d1914,native_data_021d1914+0x1000,0x1000,16);
        native_fn_0200698c(native_data_021d1914+0x111C);
    }
}
