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
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
} Record_native_data_021b8ae0;
extern Record_native_data_021b8ae0 native_data_021b8ae0;
extern u8 native_data_021b8b10[];
u32 native_main_0205f70c(u32 arg0) {
    void *temp_r2;
    u32 var_r3;

    var_r3 = -1U;
    if (arg0 < 0x10U) {
        temp_r2 = native_data_021b8b10 + (arg0 * 8);
        if ((s32) M2C_FIELD(temp_r2, s16 *, 4) >= 0) {
            native_data_021b8ae0.field_1 = 0;
            var_r3 = M2C_FIELD(temp_r2, u8 *, 6);
        } else {
            native_data_021b8ae0.field_1 = 8;
        }
    } else {
        native_data_021b8ae0.field_1 = 0xC;
    }
    return (u32) var_r3;
}
