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
extern u32 native_fn_020414c8();
extern u32 native_fn_02041538();
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_0205ff80();
extern u32 native_fn_0205ff9c();
extern u32 native_fn_02062aa0();
extern u32 native_fn_02062ad0();
extern u32 native_fn_02068ae8();
extern u32 native_fn_02068eb8();
extern u32 native_fn_0206be08();
extern u32 native_fn_0206c140();
extern u32 native_fn_ov000_022219dc();
extern u32 native_fn_ov000_02221aa4();
extern u32 native_fn_ov000_02221b50();
extern u32 native_fn_ov000_022221e4();
extern u32 native_fn_ov000_0222243c();
extern u32 native_fn_ov000_022224fc();
extern u8 native_data_ov000_0222fbd4[];
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
    u8 unknown_10[0x4];
    s32 field_14;
    s32 field_18;
} Record_native_data_ov000_02246438;
extern Record_native_data_ov000_02246438 native_data_ov000_02246438;
extern u8 native_data_ov000_02246454[];
u32 native_ov000_02221dd4(void) {
    s32 var_r2;
    u32 temp_r4;

    native_fn_ov000_022219dc();
    native_fn_02068ae8();
    native_fn_02048f1c(3, 1);
    native_fn_02048f2c(2, 1);
    native_fn_02048f3c(0, 1);
    var_r2 = 0;
    do {
        *(u32 *)(native_data_ov000_02246454 + (var_r2 * 4)) = 0x20;
        var_r2 += 1;
    } while (var_r2 < 4);
    native_fn_ov000_0222243c();
    native_fn_0205ff80(native_data_ov000_0222fbd4);
    native_fn_ov000_02221b50();
    native_fn_ov000_022224fc(native_data_ov000_02246454);
    native_fn_0205ff9c();
    native_fn_ov000_02221aa4();
    native_fn_ov000_022221e4(native_data_ov000_02246438.field_c, native_data_ov000_02246438.field_14);
    temp_r4 = native_fn_02062aa0();
    native_fn_02068eb8(2, 0, 0, (s8) (temp_r4 + native_fn_02062ad0()));
    native_fn_0206be08(0, 0);
    native_fn_0206c140();
    native_data_ov000_02246438.field_18 = 5;
    native_fn_020414c8(0x3F);
    native_fn_02041538(0, 2, 0xF);
    return 1U;
}
