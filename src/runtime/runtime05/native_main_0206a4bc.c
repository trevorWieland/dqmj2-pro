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
extern u32 native_fn_02068bf4();
extern u32 native_fn_0206be08();
extern u32 native_fn_0206be14();
extern u8 native_data_021c4968[];
extern u8 native_data_021c4a0e[];
u32 native_main_0206a4bc(s8 arg0) {
    if (arg0 != -1) {
        M2C_FIELD(native_data_021c4968, s8 *, 5) = arg0;
        *(native_data_021c4a0e + (arg0 * 0x10)) = 1;
        M2C_FIELD(native_data_021c4968, s8 *, 4) = 1;
        if (native_fn_02068bf4() != 0) {
            native_fn_0206be08(0, 0);
            native_fn_0206be14(1);
        } else {
            native_fn_0206be08(0, 1);
            native_fn_0206be08(1, 1);
        }
        return 1U;
    }
    return 0U;
}
