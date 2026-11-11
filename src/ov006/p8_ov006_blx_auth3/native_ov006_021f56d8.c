#include "context.h"

/* 0x0221C094 receives the overlay's handle for the 0x0C/-4 resource. */
extern u32 native_data_ov006_0221c094;

/* Resource allocator and the six-argument registration entry point. */
extern u32 native_ov006_02203c08(s32 id, s32 size);
extern s32 native_ov006_021f1fa8(s32 first, s32 second, u32 callback_a, u32 callback_b,
                                 u32 callback_c, s32 flags);
extern void native_fn_02008430(void);
extern void native_fn_02006b7c(s32 ticks);
/* Addresses taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_021f57cc[];
extern u8 native_ov006_021f57e0[];
extern u8 native_ov006_021f57ec[];

/* ov006 row 0x021F56D8: 76 bytes. Allocate the 0x0C/-4 resource, register three
   callbacks with the sixth-argument flags 0x800, and fail loudly unless the
   registration answers 1; then sleep ten ticks. Calls at +0x0A and +0x24 are
   Thumb; the calls at +0x2C and +0x32 target ARM code and are BLX immediates in
   the image. Unknown: what the 0x0C/-4 resource is and what the "10" tick
   delay waits for. */
void native_ov006_021f56d8(void)
{
    native_data_ov006_0221c094 = native_ov006_02203c08(0x0C, -4);
    if (native_ov006_021f1fa8(0x0F, 0x40, (u32)(native_ov006_021f57cc + 1),
                              (u32)(native_ov006_021f57e0 + 1),
                              (u32)(native_ov006_021f57ec + 1), 0x800) != 1)
        native_fn_02008430();
    native_fn_02006b7c(0x0A);
}
