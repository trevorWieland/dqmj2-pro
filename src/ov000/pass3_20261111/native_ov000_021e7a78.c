typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Probe then commit: returns 0 when the probe service reports empty.
 * 
 * The probe result is named before the result variable; that order is what keeps
 * the image's unconditional `mov r0,#0` instead of a predicated store (mwcc sinks
 * the constant when the result is only returned).
 * Unknowns: the probe at 0x0205e7f4 and the commit at 0x0205c1a8. */

extern u32 native_fn_0205e7f4(u32, u32);
extern void native_fn_0205c1a8(void);

s32 native_ov000_021e7a78(void)
{
    u32 value = native_fn_0205e7f4(0, 0);
    s32 result = 0;

    if (value != 0) {
        native_fn_0205c1a8();
        result = 1;
    }
    return result;
}
