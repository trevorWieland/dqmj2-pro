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
extern u32 native_fn_0202a164();
extern u32 native_fn_0204617c();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0205f5f4();
extern u32 native_fn_0205fd80();
extern u32 native_fn_02084f4c();
extern u32 native_fn_ov000_021d7df0();
extern u32 native_fn_ov000_02227f78();
typedef struct {
    u8 unknown_0[0x540];
    s32 field_540;
} Record_native_data_020feae8;
extern Record_native_data_020feae8 native_data_020feae8;
extern u8 native_data_ov000_0222e120[];
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
    u8 unknown_10[0xc];
    s32 field_1c;
} Record_native_data_ov000_022300c0;
extern Record_native_data_ov000_022300c0 native_data_ov000_022300c0;
extern u8 native_data_ov000_022300f8[];
u32 native_ov000_021d7550(void) {
    s32 var_r5;

    native_fn_0204617c(0, 2);
    var_r5 = 0;
    do {
        native_fn_02084f4c(*(u32 *)(native_data_ov000_022300f8 + (var_r5 * 4)));
        var_r5 += 1;
    } while (var_r5 < 2);
    native_fn_ov000_02227f78();
    native_fn_ov000_021d7df0();
    native_fn_020485b4(native_data_ov000_022300c0.field_1c);
    native_fn_020484dc(0, *native_data_ov000_0222e120);
    native_fn_0205f5f4(native_data_ov000_022300c0.field_c);
    native_data_020feae8.field_540 = 0;
    native_fn_0202a164(2);
    native_fn_0202a164(8);
    return native_fn_0205fd80(0);
}
