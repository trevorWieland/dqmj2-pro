#include "context.h"

/* 0x0221C184 holds a pointer to the ov006 resource state. The record at
   state+0x67C is special: it clears 0x6000 bytes through the two-argument
   release helper and the three-argument fill helper, while every other record
   clears 0x3000. Each record's buffer pointer is at +0x638 for the special one
   and +0x668 for the rest. */
extern u32 native_data_ov006_0221c184;

extern void native_fn_02007308(void *buffer, u32 size);
extern void native_fn_02004e58(void *buffer, s32 value, u32 size);
extern void native_fn_02004eb8(void *buffer, s32 value, u32 size);

/* ov006 row 0x022035D8: 108 bytes. Tear one resource record down when its
   caller-supplied flag byte is set: release and clear the record's buffer with
   the size that matches the special record, then clear the flag. The calls at
   +0x1E, +0x30, +0x3E and +0x50 target ARM code and are BLX immediates in the
   image. Unknown: what the first (unused) argument is for, and why the special
   record needs 0x6000 bytes where the others need 0x3000. */
void native_ov006_022035d8(u32 unused, u8 *flag)
{
    if (*flag == 0)
        return;

    if (flag == (u8 *)(native_data_ov006_0221c184 + 0x67C)) {
        native_fn_02007308((void *)(*(u32 *)(native_data_ov006_0221c184 + 0x638)), 0x6000);
        native_fn_02004e58((void *)(*(u32 *)(native_data_ov006_0221c184 + 0x638)), 0, 0x6000);
    } else {
        native_fn_02007308((void *)(*(u32 *)(native_data_ov006_0221c184 + 0x668)), 0x3000);
        native_fn_02004eb8((void *)(*(u32 *)(native_data_ov006_0221c184 + 0x668)), 0x3000,
                           0x3000);
    }
    *flag = 0;
}
