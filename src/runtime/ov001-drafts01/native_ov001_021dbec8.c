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
extern u32 native_fn_ov001_021dbe68();
u32 native_ov001_021dbec8(void *arg0) {
    u32 temp_r4;
    u32 var_r5;

    temp_r4 = native_fn_ov001_021dbe68();
    var_r5 = 1;
    if (M2C_FIELD(arg0, u8 *, 0x322) == 0) {
        if ((s32) temp_r4 <= 0x32) {
            if ((s32) (native_fn_0203d294(0x32) + 1) > (s32) temp_r4) {
                var_r5 = 0;
            }
            return var_r5;
        }
        if ((s32) temp_r4 <= 0x190) {
            if ((s32) (native_fn_0203d294(0x15E) + 0x33) > (s32) temp_r4) {
                var_r5 = 0;
            }
            return var_r5 + 1;
        }
        if ((s32) temp_r4 <= 0x320) {
            if ((s32) (native_fn_0203d294(0x190) + 0x191) > (s32) temp_r4) {
                var_r5 = 0;
            }
            return var_r5 + 2;
        }
        if ((s32) temp_r4 <= 0x4B0) {
            if ((s32) (native_fn_0203d294(0x190) + 0x321) > (s32) temp_r4) {
                var_r5 = 0;
            }
            return var_r5 + 3;
        }
        return 4U;
    }
    return (u32) M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u8 *, 0xA9);
}
