#include "context.h"

/*
 * 0x0208ed2c (44 B, Thumb, p032/2.0-base)
 *
 * Acquire the 0x0208ed58 validator for a fresh handle. 0x0208edb0 returns the
 * handle or zero; a failed acquire returns ~0x30 (0xFFFFFFCF). On success the
 * validator is built by 0x0208ebd8 with a Thumb function pointer to
 * 0x0208ed58 (+1 in the relocation addend), the handle and the selector 1,
 * then 0x0208ecbc binds it to the handle. The handle is the return value.
 *
 * Unknowns: what the handle and validator own; the meaning of selector 1.
 */

extern u32 native_fn_0208edb0();
extern u32 native_fn_0208ebd8();
extern u32 native_fn_0208ecbc();
extern u8 native_fn_0208ed58[];

s32 native_main_0208ed2c(void)
{
    u32 handle = native_fn_0208edb0();
    u32 validator;

    if (handle == 0) {
        return ~0x30;
    }
    validator = native_fn_0208ebd8(native_fn_0208ed58 + 1, handle, 1);
    native_fn_0208ecbc(handle, validator);
    return (s32)handle;
}
