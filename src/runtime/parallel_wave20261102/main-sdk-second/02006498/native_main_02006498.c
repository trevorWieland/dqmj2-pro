#include "context_00.h"
void native_main_02006498 (void)
{
    void * stackLo;
    if (native_data_main_020e33c0.field_000c) {
        return;
    }
    native_data_main_020e33c0.field_000c = 1 ;
    native_data_main_020e33c0.field_0008 = &(native_data_main_020e33c0.field_0024.current);
    native_data_main_020e33c0.field_00f4.priority = 16 ;
    native_data_main_020e33c0.field_00f4.id = 0;
    native_data_main_020e33c0.field_00f4.state = OS_THREAD_STATE_READY;
    native_data_main_020e33c0.field_00f4.next = ((void *)0) ;
    native_data_main_020e33c0.field_00f4.profiler = ((void *)0) ;
    native_data_main_020e33c0.field_0024.list = &native_data_main_020e33c0.field_00f4;
    OS_SetCurrentThread(&native_data_main_020e33c0.field_00f4);
    stackLo = (((s32)native_data_main_00001000) <= 0) ?
              (void *)((u32)native_data_main_027e0080 - ((s32)native_data_main_00001000) ) :
              (void *)((u32)(((((u32)native_data_main_027e0000) + 0x00003fc0) - 0x40) - ((s32)native_data_main_00001000)) - ((s32)native_data_main_00001000) );
    ((void) 0)               ;
    native_data_main_020e33c0.field_00f4.stackBottom = (u32)(((((u32)native_data_main_027e0000) + 0x00003fc0) - 0x40) - ((s32)native_data_main_00001000)) ;
    native_data_main_020e33c0.field_00f4.stackTop = (u32)stackLo;
    native_data_main_020e33c0.field_00f4.stackWarningOffset = 0;
    *(u32 *)(native_data_main_020e33c0.field_00f4.stackBottom - sizeof(u32)) = 0xfddb597dUL ;
    *(u32 *)native_data_main_020e33c0.field_00f4.stackTop = 0x7bf9dd5bUL ;
    OS_InitThreadQueue(&native_data_main_020e33c0.field_00f4.joinQueue);
    native_data_main_020e33c0.field_0024.isNeedRescheduling = 0 ;
    native_data_main_020e33c0.field_0024.irqDepth = 0;
    ((void) 0) ;
    ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->threadinfo_mainp = &native_data_main_020e33c0.field_0024;
    (void)native_fn_02006c38(((void *)0) );
    native_fn_020065f0(&native_data_main_020e33c0.field_0034,
                    native_fn_02006c60,
                    (void *)((void *)0) ,
                    native_data_main_020e33c0.field_01b4 + ((sizeof(u32) * 2 + 0x40) + (sizeof(u32) * 32)) / sizeof(u32),
                    ((sizeof(u32) * 2 + 0x40) + (sizeof(u32) * 32)) ,
                    31 );
    native_data_main_020e33c0.field_0034.priority = 31 + 1;
    native_data_main_020e33c0.field_0034.state = OS_THREAD_STATE_READY;
}
