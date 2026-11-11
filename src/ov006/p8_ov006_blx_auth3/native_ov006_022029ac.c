#include "context.h"

/* 0x0221C170 holds a pointer to the ov006 scene state. The two-word window the
   teardown touches is at +0x88 (three ARM helpers), the counter word at +0xE4,
   and the handle at +0x00. */
extern u32 native_data_ov006_0221c170;

/* Table handed to the first ARM helper; contents unknown. */
extern u8 native_data_ov006_0220e8d0[];

extern void native_fn_0200c1fc(u32 table);
extern void native_fn_0200baa0(u32 block);
extern void native_fn_0200b8bc(u32 block);
extern void native_fn_0200b7c8(u32 block);
extern void native_fn_0200613c(u16 value);
extern void native_ov006_02203c20(s32 *handle);

/* ov006 row 0x022029AC: 96 bytes. Tear the scene down: hand the 0x0220E8D0
   table to the first ARM helper, run three teardown helpers over the state's
   +0x88 block, forward the +0xE4 counter, zero it, release the state handle
   through the shared-lock helper, then zero and release the state slot itself.
   Calls at +0x04, +0x0E, +0x18, +0x22, +0x2E and +0x38 target ARM code; the
   final two calls are Thumb. Unknown: what the three +0x88 helpers do, and what
   the +0xE4 counter counts. */
void native_ov006_022029ac(void)
{
    native_fn_0200c1fc((u32)native_data_ov006_0220e8d0);
    native_fn_0200baa0(native_data_ov006_0221c170 + 0x88);
    native_fn_0200b8bc(native_data_ov006_0221c170 + 0x88);
    native_fn_0200b7c8(native_data_ov006_0221c170 + 0x88);
    native_fn_0200613c(*(u16 *)(native_data_ov006_0221c170 + 0xE4));
    *(u16 *)(native_data_ov006_0221c170 + 0xE4) = 0;
    native_ov006_02203c20((s32 *)native_data_ov006_0221c170);
    *(u32 *)native_data_ov006_0221c170 = 0;
    native_ov006_02203c20((s32 *)0x0221c170);
}
