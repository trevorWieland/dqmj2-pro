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
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205fd80();
extern u32 native_fn_ov000_0221c674();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x2];
    s8 field_3;
    u8 unknown_4[0x3];
    s8 field_7;
    u8 unknown_8[0x18];
    s32 field_20;
} Record_native_data_ov000_02246090;
extern Record_native_data_ov000_02246090 native_data_ov000_02246090;
typedef struct {
    s32 field_0;
    u8 unknown_4[0xc];
    s8 field_10;
} Record_native_data_ov000_022460d4;
extern Record_native_data_ov000_022460d4 native_data_ov000_022460d4;
void native_ov000_0221a2fc(void) {
    void *temp_r0;
    s8 var_r7;

    native_fn_0205fd80(1);
    var_r7 = 0;
    do {
        temp_r0 = (void *) native_fn_02049ad0(var_r7);
        M2C_FIELD(temp_r0, s8 *, 4) = 0x7F;
        M2C_FIELD(temp_r0, s8 *, 5) = 0x7F;
        M2C_FIELD(temp_r0, s32 *, 0) = 0;
        var_r7 += 1;
        M2C_FIELD(temp_r0, s8 *, 6) = -1;
    } while ((s32) var_r7 < 0x24);
    native_fn_ov000_0221c674();
    native_fn_02048f1c(1, 1);
    native_fn_02048f2c(0, 1);
    native_fn_02048f3c(2, 1);
    native_data_ov000_02246090.field_7 = 0;
    native_data_ov000_02246090.field_3 = 0;
    native_data_ov000_02246090.field_0 = 0x7F;
    native_data_ov000_022460d4.field_10 = 0;
    native_data_ov000_022460d4.field_0 = 0;
    native_data_ov000_02246090.field_20 = 0;
}
