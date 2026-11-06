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
extern u32 native_fn_02000ce8();
extern u32 native_fn_02008d78();
extern u32 native_fn_0202824c();
extern u32 native_fn_0202a090();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0203d52c();
extern u32 native_fn_0203d644();
extern u32 native_fn_0203d660();
extern u32 native_fn_020414b0();
extern u32 native_fn_0205dfac();
extern u32 native_fn_0205dfc4();
extern u32 native_fn_ov000_021d8fdc();
extern u32 native_fn_ov000_021df3f4();
extern u32 native_fn_ov000_021dfe0c();
extern u32 native_fn_ov000_021e6378();
extern u32 native_fn_ov000_021e647c();
extern u32 native_fn_ov000_021e76f8();
extern u32 native_fn_ov000_021f3644();
extern u32 native_fn_ov000_02211098();
extern u32 native_fn_ov000_02219dc8();
extern u32 native_fn_ov000_02221428();
extern u8 native_data_020ddc78[];
extern u8 native_data_02106950[];
extern u8 native_data_02106960[];
extern u8 native_data_02106970[];
u32 native_main_0205dfd8(s32 arg0) {
    native_fn_0202a090(1, 0x108000);
    M2C_FIELD(native_data_02106950, u8 *, 0) = (u8) native_fn_0202a1e0(1);
    native_fn_0202824c(native_fn_0205dfac, native_fn_0205dfc4);
    native_fn_0203d52c();
    if (arg0 == 1) {
        native_fn_0202a090(2, 0x29800);
        native_fn_0203d644();
        native_fn_0203d660();
    }
    native_fn_ov000_021e6378();
    native_fn_ov000_021df3f4();
    native_fn_ov000_021f3644();
    native_fn_ov000_021e647c();
    native_fn_ov000_021d8fdc();
    native_fn_ov000_02221428();
    native_fn_ov000_021e76f8();
    native_fn_ov000_021dfe0c();
    if (arg0 == 1) {
        native_fn_ov000_02219dc8();
    }
    native_fn_020414b0(0x3F);
    M2C_FIELD(native_data_02106950, s32 *, 4) = 0;
    M2C_FIELD(native_data_020ddc78, s8 *, 1) = 1;
    native_fn_02008d78(native_data_02106960, 0, 0x34);
    native_fn_02000ce8(native_data_02106970);
    return native_fn_ov000_02211098();
}
