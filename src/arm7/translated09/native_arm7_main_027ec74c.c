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
extern u32 native_arm7_fn_027e9c58(u32);
extern u32 native_arm7_fn_027e9cec(u32);
extern u32 native_arm7_fn_027e9cc0(u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027ec74c(void *arg0, void *arg1) {
    u16 temp_r0;

    M2C_FIELD(arg1, s16 *, 2) = 9;
    temp_r0 = M2C_FIELD(arg0, u16 *, 0x10);
    if ((u32) temp_r0 > 1U) {
        return 5U;
    }
    if ((u32) M2C_FIELD(arg0, u16 *, 0x12) > 1U) {
        return 5U;
    }
    if ((u32) M2C_FIELD(arg0, u16 *, 0x14) > 1U) {
        return 5U;
    }
    native_arm7_fn_027e9c58((u32) temp_r0);
    if (M2C_FIELD(arg0, u16 *, 0x10) == 1) {
        if (M2C_FIELD(arg0, u16 *, 0x12) == 1) {
            native_arm7_fn_027e9cec(0x8001U);
        } else {
            native_arm7_fn_027e9cec(0U);
        }
        M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x358) = (u16) M2C_FIELD(arg0, u16 *, 0x14);
    } else {
        native_arm7_fn_027e9cec(0x8000U);
        native_arm7_fn_027e9cc0(2U);
    }
    return 0U;
}
