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
extern u32 native_fn_01ffa824();
extern u32 native_fn_01ffa84c();
extern u32 native_fn_020444ec();
extern u32 native_fn_ov001_021d9f70();
typedef struct {
    u8 field_0;
    s8 field_1;
    u8 field_2;
    u8 field_3;
} Record_native_data_ov001_022355e4;
extern Record_native_data_ov001_022355e4 native_data_ov001_022355e4;
u32 native_ov001_021da1a4(void) {
    u32 temp_r4;

    if ((native_fn_020444ec() == 0) || (temp_r4 = native_fn_01ffa824(), ((u32) (u8) temp_r4 < native_fn_01ffa84c()))) {
        native_data_ov001_022355e4.field_3 = (u8) native_fn_ov001_021d9f70(0);
        native_data_ov001_022355e4.field_0 = (u8) native_fn_ov001_021d9f70(2);
        native_data_ov001_022355e4.field_2 = (u8) native_fn_ov001_021d9f70(1);
        native_data_ov001_022355e4.field_1 = (s8) native_fn_ov001_021d9f70(3);
    } else {
        native_data_ov001_022355e4.field_2 = (u8) native_fn_ov001_021d9f70(1);
        native_data_ov001_022355e4.field_1 = (s8) native_fn_ov001_021d9f70(3);
        native_data_ov001_022355e4.field_3 = (u8) native_fn_ov001_021d9f70(0);
        native_data_ov001_022355e4.field_0 = (u8) native_fn_ov001_021d9f70(2);
    }
    return native_data_ov001_022355e4.field_3 + native_data_ov001_022355e4.field_2;
}
