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
extern u32 native_fn_0204095c();
extern u32 native_fn_02040998();
extern u32 native_fn_02041188();
extern u32 native_fn_ov000_021dfb6c();
extern u32 native_fn_ov000_021dfbac();
extern u8 native_data_ov000_0222bad0[];
extern u8 native_data_ov000_0222f820[];
extern u8 native_data_ov000_02240bb4[];
u32 native_ov000_022112a8(u32 arg0) {
    u8 sp0[32];
    s32 var_r7;
    u16 temp_r9;
    u32 temp_r0;
    u32 var_r8;

    var_r8 = 0;
    var_r7 = 0;
    do {
        temp_r9 = (u16) native_fn_ov000_021dfb6c(arg0, var_r7);
        if ((temp_r9 != 0) && (native_fn_0204095c(temp_r9, native_data_ov000_02240bb4, 0xC) == 0)) {
            temp_r0 = native_fn_02040998(temp_r9, native_data_ov000_02240bb4, 0xC);
            if (temp_r0 != 0) {
                native_fn_0201d444(&sp0, native_data_ov000_0222f820, native_fn_ov000_021dfbac(temp_r9));
                if (native_fn_02041188(temp_r0, native_data_ov000_0222bad0, &sp0) != 0) {
                    var_r8 += 1;
                }
            }
        }
        var_r7 += 1;
    } while (var_r7 < 4);
    return var_r8;
}
