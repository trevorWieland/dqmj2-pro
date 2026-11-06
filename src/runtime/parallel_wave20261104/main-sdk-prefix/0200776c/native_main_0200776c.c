#include "context_00.h"
void native_main_0200776c (void)
{
    if (0x2600000 <= *(u32 *)0x027ffd9c
        && *(u32 *)0x027ffd9c < 0x2800000) {
        native_data_main_020e3644.field_0000 = *(void **)0x027ffd9c ;
    } else {
        native_data_main_020e3644.field_0000 = ((void *)0) ;
    }
    if (!native_data_main_020e3644.field_0000) {
        *(u32 *)(0x027ffd9c ) = (u32)native_fn_020077dc;
        *(u32 *)(((((u32)native_data_main_027e0000) + 0x00003fc0) + 0x1c) ) = (u32)native_fn_020077dc;
    }
    native_data_main_020e3644.field_0008 = ((void *)0) ;
}
