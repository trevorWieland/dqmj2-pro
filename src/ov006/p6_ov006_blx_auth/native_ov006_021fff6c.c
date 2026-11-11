#include "context.h"

/* 0x0221C158 holds the main-side row base pointer; +0x1374 is a fixed record
   handed to the main-module classifier. 0x0220003D is a byte pattern/string in
   main data (the literal is deliberately unaligned). */
extern u32 native_data_ov006_0221c158;
extern u8 native_data_ov006_0220003d[];

extern s32 native_fn_02012b28(const u8 *pattern, u8 *record);

/* ov006 row 0x021FFF6C: 40 bytes. Classify the fixed record at base+0x1374
   against the pattern at 0x0220003D and return whether the classifier answered
   2. The call at +0x0C targets ARM code and is a BLX immediate in the image
   (12 F6 D6 ED). Unknown: the pattern's contents and the classifier's result
   codes other than 2. */
u32 native_ov006_021fff6c(void)
{
    return native_fn_02012b28(native_data_ov006_0220003d,
                              (u8 *)native_data_ov006_0221c158 + 0x1374) == 2;
}
