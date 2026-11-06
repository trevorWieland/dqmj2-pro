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
extern u8 native_data_ov001_0222e980[];
extern u8 native_data_ov001_0222e990[];
extern u8 native_data_ov001_0222e998[];
extern u8 native_data_ov001_0222e9a4[];
extern u8 native_data_ov001_0222e9b0[];
extern u8 native_data_ov001_0222e9bc[];
extern u8 native_data_ov001_0222e9c8[];
extern u8 native_data_ov001_0222e9d4[];
extern u8 native_data_ov001_0222e9e0[];
extern u8 native_data_ov001_0222e9ec[];
extern u8 native_data_ov001_0222e9f4[];
extern u8 native_data_ov001_0222ea00[];
extern u8 native_data_ov001_0222ea08[];
extern u8 native_data_ov001_0222ea10[];
extern u8 native_data_ov001_0222ea18[];
extern u8 native_data_ov001_0222ea20[];
extern u8 native_data_ov001_0222ea28[];
extern u8 native_data_ov001_022314bc[];
extern u8 native_data_ov001_0223161c[];
u32 native_ov001_021d8828(void) {
    u8 sp0[32];
    s32 temp_r0_2;
    s32 var_r7;
    s32 var_r8;
    u32 temp_r0;
    u32 var_r4;
    void *var_r10;

    var_r4 = 0;
    native_fn_0201d444(&sp0, native_data_ov001_0222e980);
    temp_r0 = native_fn_0203cc2c(&sp0, 1);
    if (temp_r0 != 0) {
        if (M2C_FIELD(temp_r0, s32 *, 0) == 0x534F50) {
            temp_r0_2 = M2C_FIELD(temp_r0, s32 *, 4);
            var_r10 = temp_r0 + 8;
            var_r7 = 0;
            if ((temp_r0_2 > 0) && (temp_r0_2 > 0)) {
                do {
                    if (native_fn_0201d800(var_r10, native_data_ov001_0222e990) == 0) {
                        var_r8 = 0;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e998) == 0) {
                        var_r8 = 1;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9a4) == 0) {
                        var_r8 = 2;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9b0) == 0) {
                        var_r8 = 3;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9bc) == 0) {
                        var_r8 = 4;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9c8) == 0) {
                        var_r8 = 5;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9d4) == 0) {
                        var_r8 = 6;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9e0) == 0) {
                        var_r8 = 7;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9ec) == 0) {
                        var_r8 = 8;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222e9f4) == 0) {
                        var_r8 = 9;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222ea00) == 0) {
                        var_r8 = 0xA;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222ea08) == 0) {
                        var_r8 = 0xB;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222ea10) == 0) {
                        var_r8 = 0xC;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222ea18) == 0) {
                        var_r8 = 0xD;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222ea20) == 0) {
                        var_r8 = 0xE;
                    } else if (native_fn_0201d800(var_r10, native_data_ov001_0222ea28) == 0) {
                        var_r8 = 0xF;
                    } else {
                        var_r8 = -1;
                    }
                    if (var_r8 >= 0) {
                        native_fn_02008e0c(var_r10 + 0x20, native_data_ov001_0223161c + (var_r8 * 0x10), 0xC);
                        M2C_FIELD((native_data_ov001_022314bc + (var_r8 * 0x10)), s32 *, 0x16C) = (s32) M2C_FIELD(var_r10, s32 *, 0x30);
                    }
                    var_r7 += 1;
                    var_r10 += 0x48;
                } while (var_r7 < (s32) M2C_FIELD(temp_r0, s32 *, 4));
            }
            var_r4 = 1;
        }
        native_fn_0203cf9c(1, temp_r0);
    }
    return var_r4;
}
