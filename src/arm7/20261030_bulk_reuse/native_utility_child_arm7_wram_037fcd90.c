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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm7_wram_037fcd90(void *arg0, void *arg1) {
    void *temp_r1;
    void *temp_r2;

    temp_r2 = M2C_FIELD(arg1, void **, 0x10);
    temp_r1 = M2C_FIELD(arg1, void **, 0x14);
    if (temp_r2 == NULL) {
        M2C_FIELD(arg0, void **, 0x70) = temp_r1;
    } else {
        M2C_FIELD(temp_r2, void **, 0x14) = temp_r1;
    }
    if (temp_r1 == NULL) {
        M2C_FIELD(arg0, void **, 0x6C) = temp_r2;
        return (u32) arg0;
    }
    M2C_FIELD(temp_r1, void **, 0x10) = temp_r2;
    return (u32) arg0;
}
