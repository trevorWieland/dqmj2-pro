#include "context.h"

extern u8 native_data_0221c170[];
extern void native_fn_02203c20(u32 *arguments);
extern void native_fn_022030dc(u32 subrecord, u32 value);

/* Publish the four-word argument block, then forward the first argument with
   the scene subrecord at +0x84. */
void native_main_02202b24(u32 first, u32 second, u32 third, u32 fourth)
{
    native_fn_02203c20(&first);
    native_fn_022030dc(*(u32 *)((u8 *)*(u32 **)native_data_0221c170 + 0x84), first);
}
