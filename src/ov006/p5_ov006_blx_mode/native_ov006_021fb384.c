#include "context.h"

extern u8 native_data_ov006_0221c0ec[];
extern u32 native_fn_02002480(u16 value, s32 mode);

/* ov006 row 0x021FB384: 24 bytes, byte-exact with the mode-aware relocation
   application. The call at +0xA targets the ARM function 0x02002480 and is a
   BLX immediate in the image (07 F6 78 E8); mwccarm emits BL plus
   R_ARM_THM_CALL instead. Negative control: 0x1D -> 0x1E must change the
   argument immediate and fail the byte comparison. */
u32 native_ov006_021fb384(u32 value)
{
    return native_fn_02002480(*(u16 *)(native_data_ov006_0221c0ec + 4), 0x1D) - -value;
}
