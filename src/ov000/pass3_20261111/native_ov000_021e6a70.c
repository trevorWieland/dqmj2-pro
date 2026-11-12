typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Twin of 0x021e6a40 with the second lookup service.
 * 
 * Same 12-byte record copy and compound null test; only the lookup at 0x020285c8
 * differs.
 * Unknowns: what the two services resolve. */

typedef struct { u32 a; u32 b; u32 c; } Block;

extern u32 native_fn_021e63a4(u32);
extern u32 *native_fn_020285c8(u32, u32 *);

u32 *native_ov000_021e6a70(u32 value, Block *dst)
{
    u32 handle = native_fn_021e63a4(value);
    Block *src = (Block *)native_fn_020285c8(handle, (u32 *)dst);

    if (dst != 0 && src != 0)
        *dst = *src;
    return (u32 *)src;
}
