typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Six-argument forwarder that keeps the first call's result.
 * 
 * The image copies the incoming stack arguments (5th and 6th) into its own outgoing
 * stack slots, calls the worker, runs a cleanup service with 0, and returns the
 * worker result.
 * Unknowns: the worker at 0x02217bdc and the cleanup at 0x02049e0c. */

extern u32 native_fn_ov000_02217bdc(u32, u32, u32, u32, u32, u32);
extern void native_fn_02049e0c(u32);

u32 native_ov000_02217c68(u32 a, u32 b, u32 c, u32 d, u32 e, u32 f)
{
    u32 result = native_fn_ov000_02217bdc(a, b, c, d, e, f);

    native_fn_02049e0c(0);
    return result;
}
