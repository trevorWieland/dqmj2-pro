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
extern u32 native_fn_0203a090(void *);
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
} Record_native_data_021b8ae0;
extern Record_native_data_021b8ae0 native_data_021b8ae0;
extern u8 native_data_021b8af0[];
u32 native_main_0205f848(u32 arg0) {
    u32 var_r3;

    var_r3 = 0;
    native_data_021b8ae0.field_1 = 0;
    if (arg0 < 4U) {
        if ((s32) M2C_FIELD((native_data_021b8af0 + (arg0 * 8)), s16 *, 4) < 0) {
            native_data_021b8ae0.field_1 = 8;
        } else {
            var_r3 = native_fn_0203a090(native_data_021b8af0 + (arg0 * 8));
        }
    } else {
        native_data_021b8ae0.field_1 = 0xC;
    }
    return var_r3;
}
