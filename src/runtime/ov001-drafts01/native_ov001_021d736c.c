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
    u8 unknown_0[0x4c];
    s16 field_4c;
} Record_native_data_ov001_0222fd50;
extern Record_native_data_ov001_0222fd50 native_data_ov001_0222fd50;
extern u8 native_data_ov001_0222fda0[];
u32 native_ov001_021d736c(s16 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s16 var_r0;
    s32 temp_ip;
    u32 var_r4;
    void *temp_ip_2;

    var_r0 = arg0;
    var_r4 = 0;
    if (var_r0 == -1) {
        var_r0 = native_data_ov001_0222fd50.field_4c;
    }
    if ((s32) var_r0 < 0x31) {
        temp_ip = var_r0 * 0x78;
        temp_ip_2 = native_data_ov001_0222fda0 + temp_ip;
        if ((*(native_data_ov001_0222fda0 + temp_ip) != 0) && (M2C_FIELD(temp_ip_2, u8 *, 1) == 0)) {
            M2C_FIELD(temp_ip_2, s32 *, 4) = arg1;
            M2C_FIELD(temp_ip_2, s32 *, 8) = arg2;
            M2C_FIELD(temp_ip_2, s32 *, 0xC) = arg3;
            var_r4 = 1;
        }
    }
    return var_r4;
}
