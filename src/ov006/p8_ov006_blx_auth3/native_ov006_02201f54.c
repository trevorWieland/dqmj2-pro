#include "context.h"

/* 0x0221C16C holds a pointer to the ov006 frame state. The frame counter is the
   halfword at +0x648, the active flag byte at +0xA90, the pending flag byte at
   +0xA93, the queued command word at +0x204, the source block at +0xAA4 and a
   0x40-byte staging block at +0xA50; the word at +0xAC8 is handed to the Thumb
   entry point first. */
extern u32 native_data_ov006_0221c16c;

extern void native_ov006_02201804(u32 block);
/* ARM-side "current counter" query; its answer seeds the frame counter. */
extern u16 native_fn_020125bc(void);
/* ARM block copy. */
extern void native_fn_02008e0c(u32 source, u32 destination, u32 size);

/* ov006 row 0x02201F54: 104 bytes. Queue one frame: hand the +0xAC8 block to
   the Thumb entry point, mark the frame active, latch the ARM counter answer,
   copy the +0xAA4 source block into the +0xA50 staging block, clear the pending
   flag and the queued command and advance the frame counter. The call at +0x0A
   is Thumb; the calls at +0x1A and +0x32 target ARM code and are BLX immediates
   in the image. Unknown: what 0x02201804 starts and what consumes the staging
   block. */
void native_ov006_02201f54(void)
{
    native_ov006_02201804(*(u32 *)(native_data_ov006_0221c16c + 0xAC8));
    *(u8 *)(native_data_ov006_0221c16c + 0xA90) = 1;
    *(u16 *)(native_data_ov006_0221c16c + 0x648) = native_fn_020125bc();
    native_fn_02008e0c(*(u32 *)(native_data_ov006_0221c16c + 0xAA4),
                       (u32)(native_data_ov006_0221c16c + 0xA50), 0x40);
    *(u8 *)(native_data_ov006_0221c16c + 0xA93) = 0;
    *(u32 *)(native_data_ov006_0221c16c + 0x204) = 0;
    (*(u16 *)(native_data_ov006_0221c16c + 0x648))++;
}
