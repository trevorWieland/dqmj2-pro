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
extern u32 native_fn_02006924();
extern u32 native_fn_0208a610();
typedef struct {
    u8 unknown_0[0x24];
    s32 field_24;
} Record_native_data_021cfcb8;
extern Record_native_data_021cfcb8 native_data_021cfcb8;
extern u8 native_data_021cfcbc[];
u32 native_main_0208b6a8(void *arg0) {
    void *var_r0;

    var_r0 = arg0;
    if (M2C_FIELD(var_r0, u16 *, 0) == 0x12) {
        native_data_021cfcb8.field_24 = (s32) M2C_FIELD(var_r0, u16 *, 2);
        if (M2C_FIELD(var_r0, u16 *, 2) == 0) {
            native_fn_0208a610();
        }
        var_r0 = (void *) native_fn_02006924(native_data_021cfcbc);
    }
    return (u32) var_r0;
}
