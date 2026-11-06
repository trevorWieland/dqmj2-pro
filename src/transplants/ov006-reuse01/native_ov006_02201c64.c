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
extern u8 native_data_ov006_02013f5c[];
u32 native_ov006_02201c64(s32 arg0) {
    return ((u32 (*)(s32, s32, s32)) native_data_ov006_02013f5c)(M2C_FIELD(native_data_ov006_0221c164, s32 *, 4) + 0x13E0, M2C_FIELD(native_data_ov006_0221c164, s32 *, 4) + 0x1C00, arg0);
}
