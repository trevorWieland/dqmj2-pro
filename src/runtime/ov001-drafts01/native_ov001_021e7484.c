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
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b004();
extern u32 native_fn_0207b244();
extern u32 ov001_record_field_1f2_021dbd30();
extern u32 native_fn_ov001_021e2c60();
u32 native_ov001_021e7484(void *arg0, u32 arg1) {
    u32 temp_r7_2;
    u32 var_r4;
    u8 temp_r0;
    u8 temp_r7;

    var_r4 = 1;
    temp_r7 = (u8) ((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x1C) >> 0x1C);
    if (native_fn_0207b004(arg1, 1) != 0) {
        temp_r7_2 = ov001_record_field_1f2_021dbd30(arg0);
        if ((s32) temp_r7_2 < (s32) native_fn_0207b244(arg1, ov001_record_field_1f2_021dbd30(arg0), M2C_FIELD(arg0, void **, 0x1E8) + 0x46)) {
            temp_r0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u8 *, 0xA9);
            if ((temp_r0 != 0) && (temp_r0 != 5)) {
                var_r4 = 0;
            }
        }
        if (native_fn_ov001_021e2c60(M2C_FIELD(arg0, u8 *, 0x31E), M2C_FIELD(arg0, u8 *, 0x31F), arg1) != 0) {
            var_r4 = 0;
        }
    } else if ((temp_r7 == 2) && (M2C_FIELD(arg0, u8 *, 0x31E) == 0)) {
        var_r4 = 0;
    }
    return var_r4;
}
