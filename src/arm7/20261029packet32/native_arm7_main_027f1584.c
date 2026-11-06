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
extern u32 native_arm7_fn_027eac88(u32, u32, u32);
extern u32 native_arm7_fn_027ead30(u32, u32);
extern u32 native_arm7_data_0380fff4;
extern u16 native_arm7_data_0380fff0;
u32 native_arm7_main_027f1584(void) {
    u32 temp_r0;
    u32 temp_r1;
    s32 temp_r2_2;
    u16 temp_r2;
    void *temp_r4;
    s32 temp_r5;

    temp_r4 = native_arm7_data_0380fff4 + 0x344;
    temp_r2 = M2C_FIELD(temp_r4, u16 *, 0xA0);
    temp_r5 = M2C_FIELD(native_arm7_data_0380fff4, void **, 0x4AC) + 0x24 + M2C_FIELD(temp_r4, u16 *, 0x96);
    if (temp_r2 != 0) {
        temp_r1 = M2C_FIELD(temp_r4, u32 *, 0x9C);
        temp_r0 = temp_r5 + 0xA;
        if (M2C_FIELD(temp_r4, u16 *, 0xA2) & 1) {
            native_arm7_fn_027eac88(temp_r0 - 1, temp_r1, temp_r2 + 2);
            native_arm7_fn_027ead30(temp_r5 + 9, (u32) (u8) ((s32) native_arm7_data_0380fff0 >> 8));
        } else {
            native_arm7_fn_027eac88(temp_r0, temp_r1, temp_r2 + 1);
        }
    }
    M2C_FIELD(M2C_FIELD(native_arm7_data_0380fff4, void **, 0x4AC), s16 *, 0xA) = (s16) (M2C_FIELD(temp_r4, u16 *, 0x96) + 0x26 + M2C_FIELD(temp_r4, u16 *, 0xA0));
    native_arm7_fn_027ead30(temp_r5 + 1, (u32) (u8) (M2C_FIELD(temp_r4, u16 *, 0xA0) + 8));
    if (M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x690) & 4) {
        temp_r2_2 = (temp_r5 + 0xD + M2C_FIELD(temp_r4, u16 *, 0xA0)) & ~3;
        M2C_FIELD(temp_r2_2, u16 *, 0) = 0xB6B8;
        M2C_FIELD(temp_r2_2, s16 *, 2) = 0x1D46;
    }
    M2C_FIELD(temp_r4, s16 *, 0xA4) = 0;
    return 0U;
}
