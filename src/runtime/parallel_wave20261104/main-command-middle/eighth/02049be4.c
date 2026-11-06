#include "context.h"
int native_main_02049be4(EntryView *entry, u32 font, u32 field4, u32 field5, u8 arg4, u8 arg5, u8 arg6, u8 arg7, u32 arg8, s8 arg9, u32 arg10)
{
    LinkView *link = native_fn_0205fe20((s8)font);
    if (!link) return 0;
    entry->field6 = link->first;
    native_fn_0205fe74(link, font, native_data_021029c8[font], native_data_021029d0[font], arg4, arg5, arg6, arg7, arg8, arg9, arg10);
    entry->link = link;
    entry->field4 = (s8)field4;
    entry->field5 = (s8)field5;
    return 1;
}
