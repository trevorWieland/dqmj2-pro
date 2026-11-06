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
extern u32 native_fn_02008e0c();
extern u32 native_fn_0201d444();
extern u32 native_fn_0201d800();
extern u32 native_fn_0203cc2c();
extern u32 native_fn_0203cf9c();
extern u8 native_data_ov000_0222ede4[];
extern u8 native_data_ov000_0222edf4[];
u32 native_ov000_021ea450(u32 arg0, u32 arg1, s32 *arg2) {
    u8 sp0[32];
    s32 temp_r0_2;
    s32 var_r6;
    u32 temp_r0;
    void *var_r8;

    native_fn_0201d444(&sp0, native_data_ov000_0222ede4);
    temp_r0 = native_fn_0203cc2c(&sp0, arg0);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    if (M2C_FIELD(temp_r0, s32 *, 0) == 0x534F50) {
        temp_r0_2 = M2C_FIELD(temp_r0, s32 *, 4);
        var_r8 = temp_r0 + 8;
        var_r6 = 0;
        if ((temp_r0_2 > 0) && (temp_r0_2 > 0)) {
            do {
                if (native_fn_0201d800(var_r8, native_data_ov000_0222edf4) == 0) {
                    native_fn_02008e0c(var_r8 + 0x20, arg1, 0xC);
                    *arg2 = M2C_FIELD(var_r8, s32 *, 0x30);
                }
                var_r6 += 1;
                var_r8 += 0x48;
            } while (var_r6 < (s32) M2C_FIELD(temp_r0, s32 *, 4));
        }
    }
    return native_fn_0203cf9c(arg0, temp_r0);
}
