typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e05b4(void *arg0) {
    void *temp_r3;

    temp_r3 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550) + 0xE0;
    if ((M2C_FIELD(arg0, u8 *, 0) == M2C_FIELD(M2C_FIELD(native_utility_child_arm7_data_027f94f0, void **, 0x550), u8 *, 0xE0)) && (M2C_FIELD(arg0, u8 *, 1) == M2C_FIELD(temp_r3, u8 *, 1)) && (M2C_FIELD(arg0, u8 *, 2) == M2C_FIELD(temp_r3, u8 *, 2)) && (M2C_FIELD(arg0, u8 *, 3) == M2C_FIELD(temp_r3, u8 *, 3)) && (M2C_FIELD(arg0, u8 *, 4) == M2C_FIELD(temp_r3, u8 *, 4)) && (M2C_FIELD(arg0, u8 *, 5) == M2C_FIELD(temp_r3, u8 *, 5))) {
        return 1U;
    }
    return 0U;
}
