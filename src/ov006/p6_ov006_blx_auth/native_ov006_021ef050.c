#include "context.h"

/* 0x0221AB64 is an ov006-side scratch/format buffer; 0x0221AAD0 is the base of
   a table whose word at +0x0C is a function pointer. Both are main-module data
   (0x0221xxxx) reached by the overlay. */
extern u8 native_data_ov006_0221ab64[];
extern u8 native_data_ov006_0221aad0[];

extern void native_fn_0200708c(u8 *buffer, s32 size, s32 count);
extern void native_fn_02007110(u8 *buffer);

/* ov006 row 0x021EF050: 40 bytes. Guarded buffer flush: does nothing when the
   size is zero or the count is not positive, otherwise formats `size`/`count`
   into the shared buffer, calls the record-callback pointer at
   0x0221AAD0+0x0C with the size, then finishes the buffer through
   native_fn_02007110. Byte-exact with the mode-aware R_ARM_THM_CALL expansion:
   both calls at +0x0C and +0x1A target ARM code and are BLX immediates in the
   image. Unknown: the first parameter is dead in this row (it is overwritten
   before the first call); the two ARM callees' semantics are inferred only
   from the call shape. */
void native_ov006_021ef050(void *context, s32 size, s32 count)
{
    if (size == 0 || count <= 0)
        return;

    native_fn_0200708c(native_data_ov006_0221ab64, size, count);
    (*(void (**)(s32))(native_data_ov006_0221aad0 + 0x0C))(size);
    native_fn_02007110(native_data_ov006_0221ab64);
}
