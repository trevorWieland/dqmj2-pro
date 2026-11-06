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
extern u32 native_fn_0201d444();
extern u32 native_fn_0203cf20();
extern u32 native_fn_02040d18();
extern u32 native_fn_020411c4();
extern u32 native_fn_02041aa4();
extern u32 native_fn_02041af0();
extern u32 native_fn_02041b24();
extern u32 native_fn_02042fd4();
extern u8 native_data_ov001_0222ec18[];
extern u8 native_data_ov001_0222ec20[];
extern u8 native_data_ov001_0222ec2c[];
extern u8 native_data_ov001_0222ec38[];
u32 native_ov001_021e35b4(u32 arg0) {
    u8 sp0[32];
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r0_4;
    u32 var_r6;

    var_r6 = 0;
    if (arg0 < 0x981U) {
        if (native_fn_02041af0() == 0) {
            temp_r0 = native_fn_02041b24(arg0);
            if (temp_r0 != 0) {
                temp_r0_2 = native_fn_02042fd4(arg0);
                native_fn_0201d444(&sp0, native_data_ov001_0222ec18, temp_r0_2);
                temp_r0_3 = native_fn_0203cf20(native_data_ov001_0222ec20, &sp0, -1);
                M2C_FIELD(temp_r0, u32 *, 0xC) = temp_r0_3;
                if (temp_r0_3 != 0) {
                    native_fn_0201d444(&sp0, native_data_ov001_0222ec2c, temp_r0_2);
                    if (native_fn_020411c4(M2C_FIELD(temp_r0, u32 *, 0xC), temp_r0 + 4, &sp0) != 0) {
                        native_fn_0201d444(&sp0, native_data_ov001_0222ec38, temp_r0_2);
                        temp_r0_4 = native_fn_02040d18(M2C_FIELD(temp_r0, u32 *, 0xC), &sp0);
                        M2C_FIELD(temp_r0, u32 *, 8) = temp_r0_4;
                        if (temp_r0_4 != 0) {
                            native_fn_02041aa4();
                        }
                        var_r6 = 1;
                    }
                }
            }
        } else {
            var_r6 = 2;
        }
    }
    return var_r6;
}
