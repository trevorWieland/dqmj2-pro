#include "context.h"

/* 0x0221C188 holds the main-side slot pointer that the allocator returns; a
   failed allocation is completed by the panic/cleanup helper below. */
extern u32 native_data_ov006_0221c188;

extern void native_fn_02008d78(void *dst, s32 value, u32 size);
extern u32 native_fn_0202b2f0(void *buffer, u32 size, s32 mode);
extern void native_fn_02008430(void);

/* ov006 row 0x02203B94: 44 bytes. Clear a 0x40000-byte buffer, allocate the
   same span with mode 0, store the result in the main-side slot and, when the
   allocation failed (zero), run the out-of-memory helper. Calls at +0x0A and
   +0x16 target ARM code and are BLX immediates in the image
   (05 F6 EC E8 / 27 F6 A2 EB); the failure call at +0x22 is a BLX immediate too
   (04 F6 3C EC). Unknown: the allocator's mode and the helper's behaviour. */
void native_ov006_02203b94(void *buffer)
{
    native_fn_02008d78(buffer, 0, 0x40000);
    native_data_ov006_0221c188 = native_fn_0202b2f0(buffer, 0x40000, 0);
    if (native_data_ov006_0221c188 == 0)
        native_fn_02008430();
}
