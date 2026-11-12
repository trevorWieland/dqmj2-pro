typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Release-style three-service sequence.
 * 
 * The first service returns the block whose head is cleared after the second and
 * third services run. `result` is declared before the calls because the image keeps
 * the block in r4 across them.
 * Unknowns: what ids 0x13/0 and 0x12 select. */

extern u32 native_fn_02049ad0(u32);
extern void native_fn_021ef1cc(u32);
extern void native_fn_021f0448(u32);

void native_ov000_021effec(void)
{
    u32 *result = (u32 *)native_fn_02049ad0(0x13);
    native_fn_021ef1cc(0);
    native_fn_021f0448(0x12);
    result[0] = 0;
}
