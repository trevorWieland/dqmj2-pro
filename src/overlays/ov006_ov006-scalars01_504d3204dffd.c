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
extern u32 native_fn_0205e73c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205f210();
extern u32 native_fn_0205f5dc();
extern u32 native_fn_0205f5f4();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    u8 unknown_8[0x4];
    s32 field_c;
    u8 unknown_10[0x4];
    s32 field_14;
    s32 field_18;
} Record_native_data_ov006_0220d114;
extern Record_native_data_ov006_0220d114 native_data_ov006_0220d114;
extern u8 native_data_ov006_02218d90[];
u32 native_ov006_021e938c(s32 arg0) {
    if (native_data_ov006_0220d114.field_14 != arg0) {
        if ((s32) native_data_ov006_0220d114.field_18 >= 0) {
            native_fn_0205f210(native_data_ov006_0220d114.field_18, 0);
            native_data_ov006_0220d114.field_14 = -1;
            native_data_ov006_0220d114.field_18 = -1;
            native_data_ov006_0220d114.field_c = -1;
            native_data_ov006_0220d114.field_4 = -1;
        }
        native_fn_0205f5f4(*(u32 *)native_data_ov006_02218d90);
        native_fn_0205e73c(arg0);
        native_data_ov006_0220d114.field_18 = (s32) native_fn_0205e7a8(0, arg0);
        native_fn_0205f5dc();
        native_fn_0205f5f4();
        native_data_ov006_0220d114.field_14 = arg0;
        return 1U;
    }
    return 0U;
}
