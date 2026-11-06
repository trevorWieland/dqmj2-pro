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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0202a260();
extern u32 native_fn_0202a280();
extern u32 native_fn_02040820();
extern u32 native_fn_02041a48();
extern u32 native_fn_02042288();
extern u32 native_fn_02042c34();
extern u32 native_fn_020430b4();
extern u32 native_fn_ov000_021ea8d4();
extern u32 native_fn_ov000_0221108c();
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
    u8 unknown_3[0x5];
    s32 field_8;
} Record_native_data_ov000_02244efc;
extern Record_native_data_ov000_02244efc native_data_ov000_02244efc;
extern u8 native_data_ov000_02244f7c[];
extern u8 native_data_ov000_02245128[];
typedef struct {
    u8 unknown_0[0x6a];
    s16 field_6a;
    u8 unknown_6c[0x76];
    s16 field_e2;
} Record_native_data_ov000_02245228;
extern Record_native_data_ov000_02245228 native_data_ov000_02245228;
u32 native_ov000_0221452c(void) {
    s32 var_r5;
    u8 *var_r6;

    if ((s32) native_data_ov000_02245228.field_e2 <= 0) {
        return 1U;
    }
    native_fn_0202a260();
    native_fn_0202a1e0(1);
    if (native_fn_02042288(native_data_ov000_02245128) != 0) {
        var_r6 = native_data_ov000_02244f7c;
        var_r5 = 0;
loop_4:
        if (*var_r6 != 0) {
            if ((s32) M2C_FIELD((native_fn_020430b4(native_data_ov000_02245228.field_6a) + (var_r5 * 2)), s16 *, 4) > 0) {
                native_fn_02042c34();
                goto block_7;
            }
        } else {
block_7:
            var_r5 += 1;
            var_r6 += 1;
            if (var_r5 < 5) {
                goto loop_4;
            }
        }
        if (native_data_ov000_02244efc.field_2 != 0) {
            native_fn_02041a48(M2C_FIELD((void *) native_fn_020430b4(native_data_ov000_02245228.field_6a), s16 *, 2));
        }
        native_fn_ov000_021ea8d4(native_data_ov000_02244efc.field_8, 1);
    }
    native_fn_ov000_0221108c();
    native_fn_0202a280();
    native_fn_02040820();
    return 1U;
}
