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
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dc108();
u32 native_ov001_021f2304(void *arg0, u32 arg1, s32 arg2) {
    u32 temp_r4;
    void *var_r4;
    s32 var_r5;
    s32 var_r6;
    s32 var_r6_2;
    void *var_r7;

    var_r5 = -1;
    if (arg2 != 0) {
        return (u32) M2C_FIELD(arg0, u8 *, 0x31F);
    }
    temp_r4 = native_fn_ov001_021db438(M2C_FIELD(arg0, u8 *, 0x31E), 0);
    if (native_fn_0207b004(arg1, 0x8000) != 0) {
        var_r7 = temp_r4 + 0x880;
        var_r6 = 2;
        do {
            if ((native_fn_ov001_021db8d0(var_r7) != 0) && (M2C_FIELD(var_r7, s8 *, 0x257) != 0)) {
                if (native_fn_ov001_021dc108(var_r7) != 0) {
                    var_r5 = var_r6;
                }
            }
            var_r7 -= 0x440;
            var_r6 -= 1;
        } while (var_r6 >= 0);
    }
    if ((native_fn_0207b004(arg1, 8) != 0) && (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x18) >> 0x1C) != 2)) {
        var_r4 = temp_r4 + 0x880;
        var_r6_2 = 2;
        do {
            if ((native_fn_ov001_021db8d0(var_r4) != 0) && (M2C_FIELD(var_r4, s8 *, 0x251) != 0)) {
                if (native_fn_ov001_021dc108(var_r4) != 0) {
                    var_r5 = var_r6_2;
                }
            }
            var_r4 -= 0x440;
            var_r6_2 -= 1;
        } while (var_r6_2 >= 0);
    }
    if (var_r5 == -1) {
        var_r5 = (s32) M2C_FIELD(arg0, u8 *, 0x31F);
    }
    return (u32) var_r5;
}
