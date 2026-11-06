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
extern u32 native_arm7_fn_037f8988(u32, u32, u32);
extern u32 native_arm7_fn_037f8598(u32, u32);
extern u32 native_arm7_fn_037fc6d4(u32, u32, u32);
extern u32 native_arm7_fn_037f87ac(u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_wram_037f8d58(u32 arg0, u32 arg1) {
    if (M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x1FC) != 0) {
        native_arm7_fn_037f8988(arg0, native_arm7_data_0380fff4 + 0x1F4, arg1);
        return native_arm7_fn_037f8598(2U, 0x13U);
    }
    if (native_arm7_fn_037fc6d4(M2C_FIELD(native_arm7_data_0380fff4, u32 *, 0x304), arg1, 0U) != 0) {
        return native_arm7_fn_037f87ac(arg0, arg1);
    }
    return native_arm7_fn_037f8988(arg0, native_arm7_data_0380fff4 + 0x1F4, arg1);
}
