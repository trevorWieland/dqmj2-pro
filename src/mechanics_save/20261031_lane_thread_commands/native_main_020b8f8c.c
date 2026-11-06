#include "thread_commands.h"
extern u32 native_fn_020068c0(void *thread);
extern void native_fn_02006924(void *queue);
extern void native_fn_020b90bc(u32 value);
extern void native_fn_020b9270(void);
extern u8 *native_data_021d3028;

u32 native_main_020b8f8c(void) {
    if (native_data_021d3028==0) {
        return 1;
    }
    native_fn_020b90bc(2);
    if (native_fn_020068c0(native_data_021d3028+0xA10)==0) {
        native_fn_020b9270();
        return 0;
    }
    native_fn_02006924(native_data_021d3028+0xA04);
    native_data_021d3028=0;
    return 1;
}
