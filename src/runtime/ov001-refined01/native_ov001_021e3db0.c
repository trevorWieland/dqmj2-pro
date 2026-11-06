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
extern u32 native_fn_0203d294();
extern u32 native_fn_02044424();
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_0220f43c();
u32 native_ov001_021e3db0(u32 arg0, s32 arg1, s32 arg2) {
    u32 var_r0;
    u32 temp_r4;
    u32 var_r6;
    s32 var_r7;
    u32 var_r9;

    var_r9 = arg0;
    var_r6 = 1;
    if (arg1 == 0) {
        var_r7 = 0;
        do {
            temp_r4 = native_fn_ov001_021db438(0, var_r7);
            if (native_fn_ov001_021db8d0() != 0) {
                var_r9 = native_fn_ov001_0220f43c(M2C_FIELD(temp_r4, s32 *, 0x1E8) + 0x46, var_r9);
            }
            var_r7 += 1;
        } while (var_r7 < 3);
    }
    switch (var_r9) {
    default:
        break;
    case 0:
        if (arg1 != 0) {
            var_r6 = 0xFF;
        } else {
            var_r6 = 0;
        }
        break;
    case 1:
        var_r6 = native_fn_0203d294(8);
        break;
    case 2:
        var_r6 = native_fn_0203d294(0x10);
        break;
    case 3:
        var_r6 = native_fn_0203d294(0x20);
        break;
    case 4:
        var_r6 = native_fn_0203d294(0x40);
        break;
    case 5:
        var_r6 = native_fn_0203d294(0x80);
        break;
    case 6:
        var_r6 = native_fn_0203d294(0x100);
        break;
    case 7:
        var_r6 = 1;
        break;
    }
    if (arg1 != 0) {
        if ((s32) var_r6 < 4) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        return var_r0;
    }
    if ((arg2 == 0) && (native_fn_02044424(0x20000) != 0)) {
        var_r6 = 0;
    }
    if (var_r6 == 0) {
        return 1U;
    }
    return 0U;
}
