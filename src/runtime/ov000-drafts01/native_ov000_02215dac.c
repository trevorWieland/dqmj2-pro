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
extern u32 native_fn_020406dc();
extern u32 native_fn_02046150();
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205fd80();
extern u32 native_fn_020656f0();
extern u32 native_fn_020766c8();
extern u32 native_fn_ov000_021fdf98();
extern u32 native_fn_ov000_0221575c();
extern u32 native_fn_ov000_022157a0();
extern u32 native_fn_ov000_02215bc8();
extern u32 native_fn_ov000_022163fc();
extern u32 native_fn_ov000_02217500();
typedef struct {
    u8 unknown_0[0x2];
    s16 field_2;
} Record_native_data_ov000_0222f918;
extern Record_native_data_ov000_0222f918 native_data_ov000_0222f918;
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    u8 unknown_2[0x2];
    s8 field_4;
    u8 unknown_5[0x7];
    s32 field_c;
    u8 unknown_10[0x4];
    s32 field_14;
} Record_native_data_ov000_0224532c;
extern Record_native_data_ov000_0224532c native_data_ov000_0224532c;
typedef struct {
    s32 field_0;
    u8 unknown_4[0xc];
    s8 field_10;
} Record_native_data_ov000_0224536c;
extern Record_native_data_ov000_0224536c native_data_ov000_0224536c;
typedef struct {
    u8 unknown_0[0x490];
    s8 field_490;
    s8 field_491;
    u8 unknown_492[0x2];
    s8 field_494;
} Record_native_data_ov000_022459b4;
extern Record_native_data_ov000_022459b4 native_data_ov000_022459b4;
u32 native_ov000_02215dac(void) {
    s8 var_r7;
    void *temp_r0;

    native_fn_0205fd80(1);
    native_fn_020656f0();
    native_fn_ov000_022157a0();
    var_r7 = 0;
    do {
        temp_r0 = (void *) native_fn_02049ad0(var_r7);
        M2C_FIELD(temp_r0, s8 *, 4) = 0x7F;
        M2C_FIELD(temp_r0, s8 *, 5) = 0x7F;
        M2C_FIELD(temp_r0, s32 *, 0) = 0;
        var_r7 += 1;
        M2C_FIELD(temp_r0, s8 *, 6) = -1;
    } while ((s32) var_r7 < 0x24);
    native_fn_02046150(1, 0, 2);
    native_fn_02046150(2, 2, 2);
    native_fn_ov000_02217500(1);
    native_data_ov000_0224532c.field_14 = 0;
    native_fn_02048f1c(3, 1);
    native_fn_02048f2c(2, 1);
    native_fn_02048f3c(0, 1);
    native_fn_ov000_0221575c(0);
    native_data_ov000_022459b4.field_494 = 0xA;
    native_data_ov000_0224532c.field_c = 0;
    native_data_ov000_0224532c.field_1 = (s8) native_fn_020406dc();
    native_data_ov000_0224532c.field_4 = 0x7F;
    native_data_ov000_0224536c.field_10 = (s8) native_fn_020406dc();
    native_data_ov000_0224536c.field_0 = 0;
    native_data_ov000_022459b4.field_490 = 0;
    native_data_ov000_022459b4.field_491 = 0;
    native_data_ov000_0222f918.field_2 = 0x12;
    native_fn_ov000_02215bc8();
    native_fn_ov000_021fdf98();
    native_fn_020766c8();
    return native_fn_ov000_022163fc(0, 0, 0);
}
