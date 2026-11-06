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
extern u32 native_fn_02044978();
typedef struct {
    u8 unknown_0[0x4c];
    s16 field_4c;
} Record_native_data_ov001_0222fd50;
extern Record_native_data_ov001_0222fd50 native_data_ov001_0222fd50;
extern u8 native_data_ov001_0222fda0[];
u32 native_ov001_021d7814(s16 arg0, void *arg1) {
    s16 var_r0;
    s32 temp_r1;
    u8 temp_r0;
    u8 temp_r0_2;
    void *temp_ip;

    var_r0 = arg0;
    if (var_r0 == -1) {
        var_r0 = native_data_ov001_0222fd50.field_4c;
    }
    if ((s32) var_r0 >= 0x31) {
        return (u32) var_r0;
    }
    temp_r1 = var_r0 * 0x78;
    temp_r0_2 = *(native_data_ov001_0222fda0 + temp_r1);
    temp_ip = native_data_ov001_0222fda0 + temp_r1;
    if (temp_r0_2 == 0) {
        return (u32) temp_r0_2;
    }
    temp_r0 = M2C_FIELD(temp_ip, u8 *, 1);
    if (temp_r0 != 2) {
        return (u32) temp_r0;
    }
    return native_fn_02044978(temp_ip + 0x1C, M2C_FIELD(arg1, s32 *, 0), M2C_FIELD(arg1, s32 *, 4), M2C_FIELD(arg1, s32 *, 8));
}
