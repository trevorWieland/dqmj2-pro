typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_data_ov006_0221c090[];
u32 native_ov006_021f5524(void) {
    if (*native_data_ov006_0221c090 == 0) {
        return 1U;
    }
    return 0U;
}
