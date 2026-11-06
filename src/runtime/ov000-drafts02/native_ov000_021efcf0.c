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
    u8 field_0;
    s8 field_1;
} Record_native_data_ov000_02236c38;
extern Record_native_data_ov000_02236c38 native_data_ov000_02236c38;
void native_ov000_021efcf0(s32 arg0, s32 arg1) {
    u8 var_r1;
    s8 var_r1_2;

    switch (arg0) {
    case 14:
        if (arg1 != 0) {
            var_r1 = 1;
        } else {
            var_r1 = 0;
        }
        native_data_ov000_02236c38.field_0 = var_r1;
        return;
    case 15:
        if (arg1 != 0) {
            var_r1_2 = 1;
        } else {
            var_r1_2 = 0;
        }
        native_data_ov000_02236c38.field_1 = var_r1_2;
        return;
    }
}
