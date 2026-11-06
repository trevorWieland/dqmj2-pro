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
#define NULL ((void *)0)
extern u32 native_fn_02062a50(s32);
extern u32 native_fn_02062a88(s32);
extern u32 native_fn_02068bd4(u32);
extern u32 native_fn_02068c14(u32, u32, u32, u32);
extern u32 native_fn_02068f40(u32);
extern u32 native_fn_020692b0(u32, u32, u32, u8, u32, u32, u32);
extern u32 native_fn_0206c1a8(s32);
extern u32 native_fn_020bfb10(u32);
extern u32 native_fn_020bfe70(u32);
extern u32 native_fn_020c01f0(void);
extern u8 native_data_021d64b8[];

u32 native_main_020c914c(s32 arg0, s32 arg1) {
    u32 var_r9_2;
    s32 var_r10;
    s32 var_r8;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 var_r9;

    native_fn_02068bd4(M2C_FIELD(native_data_021d64b8, s32 *, 0xC));
    var_r9 = 0;
    var_r8 = 0;
    do {
        temp_r0_2 = native_fn_02062a50(var_r8);
        if (temp_r0_2 != 0) {
            native_fn_020692b0(M2C_FIELD(temp_r0_2, s32 *, 0x14), 0, 0, (u8) var_r9, 0, 0xC, 0xF);
            var_r9 += native_fn_0206c1a8(M2C_FIELD(temp_r0_2, s16 *, 0x18)) + 1;
        }
        var_r8 += 1;
    } while (var_r8 < 3);
    if (arg1 != 0) {
        var_r9_2 = 0;
        var_r10 = 0;
        do {
            temp_r0_3 = native_fn_02062a88(var_r10);
            if (temp_r0_3 != 0) {
                native_fn_020692b0(M2C_FIELD(temp_r0_3, s32 *, 0x14), 1, 0, (u8) var_r9_2, 0, 0xC, 0xF);
                var_r9_2 += native_fn_0206c1a8(M2C_FIELD(temp_r0_3, s16 *, 0x18)) + 1;
            }
            var_r10 += 1;
        } while (var_r10 < 3);
    }
    native_fn_020bfb10(0);
    native_fn_020c01f0();
    native_fn_020bfe70(M2C_FIELD(native_data_021d64b8, s32 *, 0xC));
    temp_r0 = native_fn_02068c14(2, 0x24, 0x20, 1);
    if (arg0 == 0) {
        return temp_r0;
    }
    return native_fn_02068f40(1);
}
