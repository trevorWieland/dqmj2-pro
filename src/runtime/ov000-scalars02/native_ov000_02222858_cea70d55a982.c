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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_020273d8();
extern u32 native_fn_0202a090();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0202a32c();
extern u32 native_fn_02045738();
extern u32 native_fn_020642dc();
extern u32 native_fn_0207a9ec();
extern u32 native_fn_ov000_0222290c();
extern u32 native_fn_ov000_02222a10();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    s32 field_8;
} Record_native_data_ov000_02246574;
extern Record_native_data_ov000_02246574 native_data_ov000_02246574;
extern u8 native_data_ov000_02246584[];
u32 native_ov000_02222858(void) {
    s32 var_r2;
    u32 temp_r4;

    native_data_ov000_02246574.field_8 = 8;
    native_fn_02045738(0);
    if ((native_fn_020642dc() == 0) && (native_fn_0202a32c(8) == 0)) {
        native_fn_0202a090(8, 0x8000);
    }
    native_fn_0202a090(1, 0x80000);
    temp_r4 = native_fn_0202a1e0(1U);
    native_fn_0202a090(2, 0x29800);
    native_fn_ov000_0222290c();
    native_fn_ov000_02222a10();
    native_fn_0207a9ec(2);
    native_fn_0202a1e0(temp_r4);
    native_fn_020273d8(7);
    var_r2 = 0;
    native_data_ov000_02246574.field_4 = 0;
    do {
        *(u32 *)(native_data_ov000_02246584 + (var_r2 * 4)) = 0x20;
        var_r2 += 1;
    } while (var_r2 < 4);
    return (u32) native_data_ov000_02246584;
}
