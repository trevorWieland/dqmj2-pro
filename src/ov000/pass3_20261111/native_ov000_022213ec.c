typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Advance a 1..4 mode index, notify two services, and latch two flag bytes.
 * 
 * `index + 1` wraps to 1 at 4; the image uses `movge` for the wrap. The returned
 * value is the wrapped index, and the two 0x022463b0 bytes are set after the calls.
 * Unknowns: what the mode index selects and what the two latches enable. */

extern void native_fn_0207ca3c(u32);
extern void native_fn_ov000_0221c9e4(void);
extern u8 native_data_ov000_022463b0[];

s32 native_ov000_022213ec(s32 index)
{
    index = index + 1;
    if (index >= 4)
        index = 1;
    native_fn_0207ca3c(index);
    native_fn_ov000_0221c9e4();
    M2C_FIELD(native_data_ov000_022463b0, u8 *, 0) = 1;
    M2C_FIELD(native_data_ov000_022463b0, u8 *, 1) = 1;
    return index;
}
