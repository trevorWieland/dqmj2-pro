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
extern u32 native_fn_0202a634();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov006_021e648c();
extern u32 native_fn_ov006_021e7d48();
extern u32 native_fn_ov006_021e7d78();
extern u32 native_fn_ov006_021e7e28();
extern u32 native_fn_ov006_0220692c();
extern u32 native_fn_ov006_02207034();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov006_0221c27c;
extern Record_native_data_ov006_0221c27c native_data_ov006_0221c27c;
u32 native_ov006_0220706c(s32 arg0) {
    u16 temp_r0;

    if (arg0 != 0) {
        temp_r0 = M2C_FIELD((void *) native_fn_0202a634(), u16 *, 2);
        if (temp_r0 & 1) {
            if (native_fn_ov006_021e7d48() == 0) {
                native_fn_0205e7a8(-1, 0x52);
                native_data_ov006_0221c27c.field_8 = 4;
            } else {
                native_fn_0205e7a8(-1, 0x53);
                native_data_ov006_0221c27c.field_8 = 1;
                native_fn_ov006_021e7e28();
                native_fn_ov006_0220692c();
            }
            native_fn_ov006_021e7d78();
        } else if (temp_r0 & 2) {
            native_fn_ov006_021e7d78();
            native_fn_ov006_021e7e28();
            native_fn_0205e7a8(-1, 0x53);
            native_data_ov006_0221c27c.field_8 = 1;
            native_fn_ov006_0220692c();
        }
    }
    if (native_data_ov006_0221c27c.field_8 == 3) {
        native_fn_ov006_02207034();
    }
    return native_fn_ov006_021e648c(arg0);
}
