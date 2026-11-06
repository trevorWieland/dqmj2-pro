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
extern u32 native_arm7_fn_037f8598(u32, u32);
extern u32 native_arm7_data_0380fff4;
void native_arm7_main_027eaa78(void) {
    u32 temp_r4;

    temp_r4 = native_arm7_data_0380fff4;
    M2C_FIELD(temp_r4, s32 *, 0x3EC) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x3EC) + 1);
    native_arm7_fn_037f8598(1U, 0xAU);
    native_arm7_fn_037f8598(2U, 0x12U);
    native_arm7_fn_037f8598(1U, 0x11U);
    if (M2C_FIELD(temp_r4, u16 *, 0x1FC) != 0) {
        native_arm7_fn_037f8598(2U, 0x13U);
    }
    if (M2C_FIELD(temp_r4, u16 *, 0x3F4) != 0) {
        native_arm7_fn_037f8598(2U, 0x15U);
    }
}
