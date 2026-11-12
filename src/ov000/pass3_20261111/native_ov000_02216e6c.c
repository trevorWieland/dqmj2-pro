typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Flag-gated update: both the update call and the notification are inside the test.
 * 
 * The image branches past the notification when the 0xff7 bits are clear, so the
 * second call is inside the if, not after it.
 * Unknowns: what field +2 marks and what the notification reports. */

extern u32 native_fn_0202a634(void);
extern void native_fn_ov000_02216cc8(void);
extern void native_fn_02068f60(u32);

s32 native_ov000_02216e6c(void)
{
    u8 *object = (u8 *)native_fn_0202a634();
    s32 result = 0;

    if (M2C_FIELD(object, u16 *, 2) & 0xff7) {
        native_fn_ov000_02216cc8();
        result = 1;
        native_fn_02068f60(result);
    }
    return result;
}
