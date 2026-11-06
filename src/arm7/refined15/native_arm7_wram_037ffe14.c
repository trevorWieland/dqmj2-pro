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
extern u32 native_arm7_fn_037fee58(u32, u32);
u32 native_arm7_wram_037ffe14(void *arg0) {
    u16 temp_r1;

    if (M2C_FIELD(arg0, u8 *, 2) == 0) {
        return 0U;
    }
    temp_r1 = M2C_FIELD(arg0, u16 *, 6);
    if ((u32) temp_r1 < (u32) M2C_FIELD(arg0, u16 *, 4)) {
        return 0U;
    }
    return M2C_FIELD(arg0, u8 *, 3) * (M2C_FIELD(arg0, u8 *, 2) * native_arm7_fn_037fee58((u32) (u16) M2C_FIELD(arg0, u16 *, 8) >> 8, (u32) temp_r1));
}
