#include "context.h"

/* Report whether the frame layout table entry is the two-entry marker. */
s32 native_ov006_021feb34(void)
{
    return native_fn_02012b28((u8 *)0x021FEC01, native_data_ov006_0221c144 + 0x1648) == 2;
}
