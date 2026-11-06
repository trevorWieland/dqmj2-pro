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

u32 native_utility_child_arm7_wram_037fd6c4(u32 arg0, void *arg1) {
    void *temp_r2;
    void **temp_r3;

    temp_r3 = M2C_FIELD(arg1, void ***, 4);
    if (temp_r3 != NULL) {
        *temp_r3 = M2C_FIELD(arg1, void **, 0);
    }
    temp_r2 = M2C_FIELD(arg1, void **, 0);
    if (temp_r2 == NULL) {
        return (u32) M2C_FIELD(arg1, void ***, 4);
    }
    M2C_FIELD(temp_r2, void ***, 4) = (void **) M2C_FIELD(arg1, void ***, 4);
    return arg0;
}
