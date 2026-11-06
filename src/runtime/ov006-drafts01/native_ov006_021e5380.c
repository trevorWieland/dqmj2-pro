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
extern u32 native_fn_020b9f74();
extern u32 native_fn_020bae44();
extern u32 native_fn_ov006_021e3cd4();
extern u32 native_fn_ov006_021e3f28();
extern u32 native_fn_ov006_021e4b24();
extern u32 native_fn_ov006_021e537c();
extern u32 native_fn_ov006_021e7d98();
extern u32 native_fn_ov006_021e7fe0();
extern u32 native_fn_ov006_021e9148();
extern u8 native_data_ov006_02207d24[];
extern u8 native_data_ov006_02218d54[];
u32 native_ov006_021e5380(void) {
    native_fn_020bae44();
    native_fn_ov006_021e4b24();
    if (native_fn_020b9f74(native_data_ov006_02218d54, native_fn_ov006_021e537c, 0) != 0) {
        native_fn_ov006_021e7fe0();
        native_fn_ov006_021e7d98(0);
        native_fn_ov006_021e9148(native_data_ov006_02207d24, 0);
    } else {
        native_fn_ov006_021e3f28(2);
    }
    return native_fn_ov006_021e3cd4();
}
