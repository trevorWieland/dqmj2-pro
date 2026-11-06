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
extern u32 native_arm7_fn_037f886c(u32, u32);
extern u32 native_arm7_fn_027eac0c(u32, u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_wram_037fae50(u32 arg0, s32 arg1) {
    u32 temp_r0;

    temp_r0 = native_arm7_fn_037f886c(native_arm7_data_0380fff4 + 0x188, arg1 + 0x22);
    if (temp_r0 == 0) {
        return 0U;
    }
    native_arm7_fn_027eac0c(temp_r0 + 0x18, arg0, arg1 + 0xC);
    M2C_FIELD(temp_r0, s16 *, 0x16) = (s16) (arg1 - 0x18);
    M2C_FIELD(temp_r0, u16 *, 0x1E) = (u16) ((u8) M2C_FIELD(temp_r0, u16 *, 0x1E) | ((u32) ((u8) M2C_FIELD(temp_r0, u16 *, 0x22) << 0x10) >> 8));
    return temp_r0 + 0x10;
}
