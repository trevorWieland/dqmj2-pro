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
extern u32 native_fn_02068830();
extern u32 native_fn_ov006_021e3cd8();
extern u32 native_fn_ov006_021e3f28();
extern u32 native_fn_ov006_021e65a4();
extern u32 native_fn_ov006_021e802c();
extern u8 native_data_ov006_0220d108[];
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov006_02218d70;
extern Record_native_data_ov006_02218d70 native_data_ov006_02218d70;
extern u8 native_data_ov006_02218d7c[];
u32 native_ov006_021e6044(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov006_021e65a4();
    switch (temp_r0) {
    case -2:
        *(u32 *)native_data_ov006_0220d108 = native_fn_02068830(native_data_ov006_02218d7c);
        native_fn_ov006_021e3f28(0x63);
        break;
    case -1:
        native_fn_ov006_021e802c(3);
        if (native_data_ov006_02218d70.field_4 != 0) {
            native_fn_ov006_021e3f28(0x62);
        } else {
            native_fn_ov006_021e3f28(3);
        }
        break;
    }
    return native_fn_ov006_021e3cd8();
}
