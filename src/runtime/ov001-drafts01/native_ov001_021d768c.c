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
extern u32 native_fn_02044890();
typedef struct {
    u8 unknown_0[0x4c];
    s16 field_4c;
} Record_native_data_ov001_0222fd50;
extern Record_native_data_ov001_0222fd50 native_data_ov001_0222fd50;
extern u8 native_data_ov001_0222fda0[];
u32 native_ov001_021d768c(s16 arg0, u32 arg1, u32 arg2, u32 arg3) {
    s16 var_r0;
    s32 temp_r1;
    u32 var_r3;
    void *temp_r1_2;

    var_r0 = arg0;
    var_r3 = arg3;
    if (var_r0 == -1) {
        var_r0 = native_data_ov001_0222fd50.field_4c;
    }
    if ((s32) var_r0 < 0x31) {
        temp_r1 = var_r0 * 0x78;
        temp_r1_2 = native_data_ov001_0222fda0 + temp_r1;
        if ((*(native_data_ov001_0222fda0 + temp_r1) != 0) && (M2C_FIELD(temp_r1_2, u8 *, 1) == 2)) {
            var_r3 = native_fn_02044890(temp_r1_2 + 0x1C);
        }
    }
    return var_r3;
}
