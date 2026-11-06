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
extern u32 native_fn_0202bd74();
extern u32 native_fn_02041dbc();
extern u32 native_fn_02041e50();
extern u8 native_data_ov001_0222deec[];
u32 native_ov001_021d9424(void *arg0, u32 arg1, u32 arg2) {
    s32 temp_r0;
    s32 var_r0;
    u32 var_r0_2;

    if (native_fn_02041e50() != 0) {
        native_fn_02041dbc(arg0 + 0x100, arg0, arg2);
        temp_r0 = M2C_FIELD(arg0, s32 *, 0x10);
        if (temp_r0 != 0) {
            var_r0 = temp_r0 + 0x40;
        } else {
            var_r0 = 0;
        }
        if (var_r0 == 0) {
            var_r0_2 = -1U;
        } else {
            var_r0_2 = native_fn_0202bd74(var_r0, native_data_ov001_0222deec);
        }
        M2C_FIELD(arg0, u32 *, 0x1E0) = var_r0_2;
        M2C_FIELD(arg0, s8 *, 0x15E) = 1;
        M2C_FIELD(arg0, s8 *, 0x160) = 0x1F;
        return 1U;
    }
    return 0U;
}
