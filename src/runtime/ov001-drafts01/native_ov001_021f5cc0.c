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
extern u32 native_fn_ov001_021d96d4();
extern u32 native_fn_ov001_021db438();
u32 native_ov001_021f5cc0(void *arg0, u32 arg1) {
    s32 var_r1;
    s32 var_r4;
    s32 var_r5;
    u32 var_r6;
    void *var_r7;

    var_r7 = arg0;
    var_r6 = 1;
    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x10) >> 0x1C) != 1) {
        var_r5 = 1;
    } else {
        var_r7 = (void *) native_fn_ov001_021db438(M2C_FIELD(var_r7, u8 *, 0x31E), 0);
        var_r5 = 3;
    }
    var_r4 = 0;
    if ((var_r5 > 0) && (var_r5 > 0)) {
        do {
            if (((u32) M2C_FIELD(var_r7, u8 *, 0x160) < 0x1FU) && (M2C_FIELD(var_r7, u8 *, 0x31D) != 0)) {
                var_r1 = M2C_FIELD(var_r7, s16 *, 0x320) * 2;
                if (var_r1 > 0x1F) {
                    var_r1 = 0x1F;
                } else {
                    var_r6 = 0;
                }
                native_fn_ov001_021d96d4(var_r7, (u8) var_r1);
            }
            var_r4 += 1;
            var_r7 += 0x440;
        } while (var_r4 < var_r5);
    }
    return var_r6;
}
