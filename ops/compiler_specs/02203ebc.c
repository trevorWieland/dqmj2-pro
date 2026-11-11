typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u16 native_data_027fffa8;
extern u8 native_data_ov006_0221c18c[];

/* Report whether the caller's mask is fully set, unless the status gate is up. */
s32 native_ov006_02203ebc(u32 mask)
{
    u32 field;

    if ((native_data_027fffa8 & 0x8000) >> 15)
        return 0;
    field = *(u16 *)(*(u8 **)(native_data_ov006_0221c18c + 4) + 0x32);
    field &= mask;
    return field == mask;
}
