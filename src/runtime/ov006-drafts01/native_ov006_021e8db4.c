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
extern u32 native_fn_ov006_021e802c();
extern u32 native_fn_ov006_021e806c();
extern u32 native_fn_ov006_021e9268();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    u8 unknown_8[0x8];
    s32 field_10;
    u8 unknown_14[0x48];
    s32 field_5c;
} Record_native_data_ov006_02218d90;
extern Record_native_data_ov006_02218d90 native_data_ov006_02218d90;
u32 native_ov006_021e8db4(u32 arg0, u32 arg1, u32 arg2) {
    u16 temp_r0;
    u32 temp_r4;
    u32 var_r5;

    temp_r4 = native_fn_0202a634();
    var_r5 = native_fn_ov006_021e648c(arg2);
    if (native_data_ov006_02218d90.field_4 == 0) {
        temp_r0 = M2C_FIELD(temp_r4, u16 *, 2);
        if (temp_r0 & 1) {
            if (native_data_ov006_02218d90.field_10 != 0) {
                native_fn_0205e7a8(-1, 0x52);
            }
            if (native_data_ov006_02218d90.field_5c != 0) {
                var_r5 = -4U;
            } else {
                var_r5 = -3U;
            }
            native_fn_ov006_021e9268();
            native_fn_ov006_021e806c();
        } else if (temp_r0 & 2) {
            native_fn_0205e7a8(-1, 0x53);
            var_r5 = -4U;
            native_fn_ov006_021e9268();
            native_fn_ov006_021e806c();
        } else {
            native_fn_ov006_021e7d48();
            native_fn_ov006_021e802c();
        }
    }
    return var_r5;
}
