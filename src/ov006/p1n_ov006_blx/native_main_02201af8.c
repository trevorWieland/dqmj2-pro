#include "context.h"

extern void native_fn_02201270(u32 value);
extern void native_fn_02008430(void);

/* ov006 row 0x02201af8: 20 bytes. The only cross-mode call is a Thumb BLX
   immediate to the ARM function at 0x02008430. mwccarm emits a Thumb BL with
   an R_ARM_THM_CALL relocation; applying that relocation with the ARM
   interworking rule (BL -> BLX when the target symbol is ARM) reproduces the
   image exactly. See docs/platform/thumb-blx.md. */
void native_main_02201af8(u8 *object)
{
    if (*(u16 *)(object + 2) == 8) {
        native_fn_02201270(9);
        native_fn_02008430();
    }
}
