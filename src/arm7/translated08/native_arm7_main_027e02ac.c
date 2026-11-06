typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_data_027f8884;
u32 native_arm7_main_027e02ac(void *arg0) {
    if ((M2C_FIELD(arg0, u8 *, 0) == M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550), u8 *, 0xE0)) && (M2C_FIELD(arg0, u8 *, 1) == M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550), u8 *, 0xE1)) && (M2C_FIELD(arg0, u8 *, 2) == M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550), u8 *, 0xE2)) && (M2C_FIELD(arg0, u8 *, 3) == M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550), u8 *, 0xE3)) && (M2C_FIELD(arg0, u8 *, 4) == M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550), u8 *, 0xE4)) && (M2C_FIELD(arg0, u8 *, 5) == M2C_FIELD(M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550), u8 *, 0xE5))) {
        return 1U;
    }
    return 0U;
}
