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
extern u32 native_fn_020444a8();
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b674();
extern u32 native_fn_0207d5a0();
extern u32 native_fn_ov001_021dbcbc();
extern u32 native_fn_ov001_021dbd24();
extern u32 native_fn_ov001_021dbe68();
extern u32 native_fn_ov001_021f24d8();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_021f2550(void *arg0, u32 arg1) {
    s32 temp_r0;
    s32 temp_r0_2;
    u32 temp_r4;
    u32 var_r4;
    u32 var_r5;

    var_r4 = 0;
    if ((M2C_FIELD(arg0, s8 *, 0x244) == 0) && (native_fn_ov001_021f24d8(arg1) != 0)) {
        temp_r0 = (s32) native_fn_ov001_021dbe68(arg0);
        if (temp_r0 >= 0x3E8) {
            var_r5 = 0x10;
        } else if (temp_r0 >= 0x320) {
            var_r5 = 0xC;
        } else if (temp_r0 >= 0x258) {
            var_r5 = 0xA;
        } else if (temp_r0 >= 0x190) {
            var_r5 = 8;
        } else if (temp_r0 >= 0xC8) {
            var_r5 = 6;
        } else if (temp_r0 >= 0x64) {
            var_r5 = 4;
        } else if (temp_r0 >= 0x32) {
            var_r5 = 2;
        } else {
            var_r5 = 1;
        }
        if ((s32) native_fn_0207b674(0xEA, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) {
            var_r5 *= 2;
        }
        if ((s32) native_fn_0207b674(0xEB, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) {
            temp_r4 = native_fn_ov001_021dbd24(arg0);
            temp_r0_2 = (s32) native_fn_ov001_021dbcbc(arg0);
            if ((s32) temp_r4 <= (s32) ((s32) (temp_r0_2 + ((u32) (temp_r0_2 >> 2) >> 0x1D)) >> 3)) {
                var_r5 *= 0x10;
            } else if ((s32) temp_r4 <= (s32) ((s32) (temp_r0_2 + ((u32) (temp_r0_2 >> 1) >> 0x1E)) >> 2)) {
                var_r5 *= 8;
            }
        }
        if ((native_fn_020444a8() == 0) && (M2C_FIELD(arg0, u8 *, 0x31E) == 1)) {
            var_r5 = (u32) ((s32) (var_r5 + (var_r5 >> 0x1F)) >> 1);
        }
        var_r4 = native_fn_ov001_02210ad0(arg0, 0x100, native_fn_0207d5a0(M2C_FIELD(arg0, u8 *, 0x1FD), (s32) var_r5, (u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x1C) >> 0x1C));
    }
    return var_r4;
}
