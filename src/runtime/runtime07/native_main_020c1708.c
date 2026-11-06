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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02069000();
extern u32 native_fn_0206c078();
extern u32 native_fn_0207ca3c();
extern u32 native_fn_020bfb10();
extern u32 native_fn_020c01f0();
extern u32 native_fn_020c0210();
extern u32 native_fn_020c1794();
extern u8 native_data_021d4bec[];
u32 native_main_020c1708(s32 *arg0) {
    s32 temp_r0;
    u32 temp_r4;

    if (native_fn_020c1794() == 0) {
        temp_r0 = *arg0 + 1;
        *arg0 = temp_r0;
        if (temp_r0 >= 4) {
            *arg0 = 1;
        }
        native_fn_0207ca3c(*arg0);
        temp_r4 = native_fn_0206c078();
        if (M2C_FIELD(temp_r4, s8 *, 0) == native_fn_02069000()) {
            M2C_FIELD(native_data_021d4bec, s8 *, 4) = 0;
            if (M2C_FIELD(temp_r4, u8 *, 6) == 0) {
                M2C_FIELD(temp_r4, s8 *, 2) = 0;
                M2C_FIELD(temp_r4, s8 *, 3) = 0;
            }
        }
        native_fn_020c0210();
        native_fn_020bfb10(0);
        native_fn_020c01f0();
        return 1U;
    }
    return 0U;
}
