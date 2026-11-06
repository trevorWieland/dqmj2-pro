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
extern u32 native_fn_0202b594();
u32 native_main_0202b7e4(void *arg0, s32 arg1) {
    s32 temp_r4;
    u32 temp_r0;

    temp_r4 = M2C_FIELD(arg0, s32 *, 0x24);
    temp_r0 = native_fn_0202b594(arg0 + 0x24, 0x10, 4);
    if (temp_r0 == 0) {
        return 0U;
    }
    M2C_FIELD(temp_r0, s32 *, 0) = arg1;
    M2C_FIELD(temp_r0, s32 *, 4) = temp_r4;
    M2C_FIELD(temp_r0, s32 *, 8) = (s32) M2C_FIELD(arg0, s32 *, 0x28);
    M2C_FIELD(temp_r0, u32 *, 0xC) = (u32) M2C_FIELD(arg0, u32 *, 0x2C);
    M2C_FIELD(arg0, u32 *, 0x2C) = temp_r0;
    return 1U;
}
