typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Look up a 12-byte record and copy it into the caller's block.
 * 
 * The image compares the destination and the lookup result with `cmpne` (a compound
 * test), copies with `ldm`/`stm`, and returns the lookup pointer.
 * Unknowns: what the two services resolve. */

typedef struct { u32 a; u32 b; u32 c; } Block;

extern u32 native_fn_021e63a4(u32);
extern u32 *native_fn_0202859c(u32, u32 *);

u32 *native_ov000_021e6a40(u32 value, Block *dst)
{
    u32 handle = native_fn_021e63a4(value);
    Block *src = (Block *)native_fn_0202859c(handle, (u32 *)dst);

    if (dst != 0 && src != 0)
        *dst = *src;
    return (u32 *)src;
}
