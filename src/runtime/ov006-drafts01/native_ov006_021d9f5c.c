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
extern u32 native_fn_0203d2dc();
extern u32 native_fn_020443d4();
extern u32 native_fn_02044454();
extern u32 native_fn_02064978();
extern u32 native_fn_02064b24();
extern u32 native_fn_02064c8c();
extern u32 native_fn_02064d64();
extern u32 native_fn_02065170();
extern u32 native_fn_020652dc();
extern u32 native_fn_02065304();
extern u32 native_fn_02065608();
extern u32 native_fn_02065630();
extern u32 native_fn_02065648();
extern u32 native_fn_02067af4();
extern u32 native_fn_02067b08();
extern u32 native_fn_02067bd4();
extern u32 native_fn_02067bec();
extern u32 native_fn_02067cb4();
extern u32 native_fn_ov006_021d83c8();
extern u32 native_fn_ov006_021d83e4();
extern u32 native_fn_ov006_021d9ed8();
extern u8 native_data_ov006_0220f2f4[];
u32 native_ov006_021d9f5c(void) {
    s32 var_r4;
    s32 var_r5;

    native_fn_02067bd4(*M2C_FIELD(native_data_ov006_0220f2f4, u8 **, 4));
    native_fn_ov006_021d83c8();
    native_fn_02067cb4(*M2C_FIELD(native_data_ov006_0220f2f4, u8 **, 4));
    native_fn_020443d4(4);
    native_fn_02044454(0x07000046);
    var_r4 = 0;
    if ((s32) native_fn_02067b08() > 0) {
        do {
            native_fn_02067af4(var_r4);
            native_fn_ov006_021d9ed8();
            var_r4 += 1;
        } while (var_r4 < (s32) native_fn_02067b08());
    }
    var_r5 = 0;
    do {
        native_fn_02067bec(*M2C_FIELD(native_data_ov006_0220f2f4, u8 **, 4), var_r5);
        native_fn_ov006_021d9ed8();
        var_r5 += 1;
    } while (var_r5 < 3);
    native_fn_02064978();
    native_fn_020652dc(0x68);
    native_fn_02065648(0x2D);
    native_fn_02065304(0);
    native_fn_0203d2dc();
    native_fn_02065608();
    native_fn_02064b24(0, 0, 0);
    native_fn_02064d64(0, 0, 0);
    native_fn_02064c8c(-1, -1, -1);
    native_fn_02065170(-1, -1, -1);
    native_fn_02065630(0);
    return native_fn_ov006_021d83e4();
}
