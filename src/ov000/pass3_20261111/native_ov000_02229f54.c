typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Signed halfword lookup in the 0x0222ffd4 table.
 * 
 * The image shifts the signed index left by one and uses a signed halfword load,
 * so the table element is `s16` and the index is a plain 32-bit argument.
 * Unknowns: the table's meaning. */

extern s16 native_data_ov000_0222ffd4[];

s32 native_ov000_02229f54(s32 index)
{
    return native_data_ov000_0222ffd4[index];
}
