typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_data_ov006_0221c164[];
u32 native_ov006_022012c0(u32 arg0) {
    if ((u32) (M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), s32 *, 0x40) - 9) > 1U) {
        M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), u32 *, 0x54) = arg0;
    }
    return arg0;
}
