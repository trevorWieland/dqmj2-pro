typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Or of four probe services.
 * 
 * The first result starts from an explicit 0 and is combined with `|=`: the image
 * emits `orr r4, r0, #0` for that first combination instead of a plain move.
 * Unknowns: what the ids 6/0xc/0xd and the final service report. */

extern u32 native_fn_ov000_021e722c(u32);
extern u32 native_fn_ov000_021e729c(void);

u32 native_ov000_021e725c(void)
{
    u32 value = 0;

    value |= native_fn_ov000_021e722c(6);
    value |= native_fn_ov000_021e722c(0xc);
    value |= native_fn_ov000_021e722c(0xd);
    return value | native_fn_ov000_021e729c();
}
