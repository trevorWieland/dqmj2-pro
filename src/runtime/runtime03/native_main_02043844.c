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
extern u32 native_fn_0203d2ec();
extern u32 native_fn_02044508();
extern u32 native_fn_0204457c();
extern u32 native_fn_ov001_021d9710();
extern u32 native_fn_ov001_021f92d8();
extern u32 native_fn_ov001_0220268c();
extern u32 native_fn_ov001_0220345c();
extern u32 native_fn_ov001_0220b3bc();
extern u32 native_fn_ov001_0220b48c();
extern u32 native_fn_ov001_0220b634();
extern u32 native_fn_ov001_022139e8();
extern u8 native_data_020f69c4[];
u32 native_main_02043844(void) {
    native_fn_ov001_021d9710();
    native_fn_ov001_021f92d8();
    native_fn_ov001_0220b48c();
    native_fn_ov001_0220b634();
    native_fn_ov001_0220b3bc();
    native_fn_ov001_022139e8(0);
    native_fn_ov001_0220268c(0);
    if (native_fn_02044508() != 0) {
        native_fn_0204457c();
        native_fn_0203d2ec();
        native_fn_ov001_0220345c(1);
    }
    M2C_FIELD(native_data_020f69c4, u8 *, 0) = 1;
    M2C_FIELD(native_data_020f69c4, s8 *, 3) = 3;
    return 1U;
}
