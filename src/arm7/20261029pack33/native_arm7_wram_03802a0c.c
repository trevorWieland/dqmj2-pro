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
extern u32 native_arm7_fn_03802860(u32, u32, u32, u32);
extern u32 native_arm7_data_038090c0;
extern u8 native_arm7_data_03802924;
u32 native_arm7_wram_03802a0c(u32 arg0, s32 arg1) {
    s32 temp_r2;
    s32 sp0;

    temp_r2 = M2C_FIELD(native_arm7_data_038090c0, s32 *, 0x28);
    switch (temp_r2) {
    case 1:
        sp0 = (arg1 | ((arg0 >> 5) & 8)) | ((arg0 & 0xFFU) << 8);
        break;
    case 2:
        sp0 = arg1 | (arg0 & 0xFF00) | ((u32) (arg0 << 0x18) >> 8);
        break;
    case 3:
        sp0 = arg1 | ((arg0 >> 8) & 0xFF00) | ((arg0 & 0xFF00) << 8) | (arg0 << 0x18);
        break;
    }
    return native_arm7_fn_03802860((u32) &sp0, 0U, temp_r2 + 1, (u32) (u32) &native_arm7_data_03802924);
}
