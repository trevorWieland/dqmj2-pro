typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u8 native_data_ov006_0221c0ec[];
extern u32 native_fn_02002480(u16 value, s32 mode);

/* Scale the caller's value by the block's current mode. */
u32 native_ov006_021fb384(u32 value)
{
    return native_fn_02002480(*(u16 *)(native_data_ov006_0221c0ec + 4), 0x1D) - -value;
}
