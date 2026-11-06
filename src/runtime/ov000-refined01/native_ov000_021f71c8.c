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
extern u32 native_fn_02045ed0();
extern u32 native_fn_02061250();
extern u32 native_fn_02061944();
extern u32 native_fn_ov000_021f72d0();
extern u32 native_fn_ov000_021f7514();
extern u32 native_fn_ov000_021f76e0();
extern u32 native_fn_ov000_021f776c();
extern u32 native_fn_ov000_021f7f7c();
extern u32 native_fn_ov000_021f7f8c();
typedef struct {
    s32 field_0;
    s32 field_4;
} Record_native_data_ov000_02236f0c;
extern Record_native_data_ov000_02236f0c native_data_ov000_02236f0c;
u32 native_ov000_021f71c8(void) {
    s8 temp_r0_2;
    s8 temp_r0_3;
    void *temp_r0;
    u32 var_r5;

    temp_r0 = (void *) native_fn_02061944();
    temp_r0_2 = M2C_FIELD(temp_r0, s8 *, 0x26A);
    var_r5 = 0;
    switch (temp_r0_2) {
    case 0:
        native_fn_ov000_021f7514();
        native_fn_02061250(0);
        native_fn_02045ed0();
        native_fn_ov000_021f72d0();
        M2C_FIELD(temp_r0, s8 *, 0x26A) = 1;
        break;
    case 1:
        if (native_data_ov000_02236f0c.field_4 == 1) {
            native_fn_ov000_021f76e0();
            native_fn_ov000_021f7f7c(0);
        } else if (native_data_ov000_02236f0c.field_0 != 0) {
            native_fn_ov000_021f776c();
            native_fn_ov000_021f7f8c(0);
        }
        temp_r0_3 = M2C_FIELD(temp_r0, s8 *, 0x26C);
        if (temp_r0_3 == 0) {
            M2C_FIELD(temp_r0, s8 *, 0x26C) = 0x2A;
        } else if (temp_r0_3 != 0x2A) {
            var_r5 = 1;
        }
        break;
    }
    return var_r5;
}
