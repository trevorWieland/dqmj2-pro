typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Two-stage predicate over signed 16-bit coordinates.
 * 
 * Both coordinate arguments are narrowed and sign-extended explicitly, which is
 * what the image's lsl/asr pairs are: the parameters are 32-bit, and the s16 casts
 * happen in the call to the first service. The second service receives its result.
 * Unknowns: what the two services test. */

extern u32 native_fn_02211104(u32, u32);
extern u32 native_fn_02211644(u32, u32);

s32 native_ov000_0221221c(s32 a, s32 b, u32 c)
{
    s32 result = 0;
    u32 handle = native_fn_02211104((s16)a, (s16)b);

    if (handle != 0) {
        if (native_fn_02211644(handle, c) != 0)
            result = 1;
    }
    return result;
}
