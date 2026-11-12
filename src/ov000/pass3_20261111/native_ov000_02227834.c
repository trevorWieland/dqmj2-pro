typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Iterate a signed byte index 0..3 through two services, then finish.
 * 
 * The increment is `(s8)(i + 1)` (lsl #24/asr #24), so the loop variable is a signed
 * byte. The loop is a `do`-while, as the image's bottom test shows.
 * Unknowns: what the per-index service and the final id 7 command do. */

extern u32 native_fn_ov000_02223c14(u32);
extern void native_fn_020c4928(u32, u32);
extern void native_fn_020c5f48(u32);

void native_ov000_02227834(void)
{
    s8 i = 0;

    do {
        u32 value = native_fn_ov000_02223c14(i);
        native_fn_020c4928(i & 0xff, value);
        i++;
    } while (i < 4);
    native_fn_020c5f48(7);
}
