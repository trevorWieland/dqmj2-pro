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
u32 native_ov001_021f24d8(u32 arg0) {
    u32 temp_r0;
    u32 temp_r5;
    u32 temp_r6;
    u32 var_r4;

    var_r4 = 0;
    temp_r5 = (u32) (M2C_FIELD((void *) native_fn_0207afec(), u16 *, 8) << 0x1C) >> 0x1C;
    temp_r6 = (u32) (M2C_FIELD((void *) native_fn_0207afec(arg0), u16 *, 8) << 0x14) >> 0x1C;
    temp_r0 = (u32) (M2C_FIELD((void *) native_fn_0207afec(arg0), u16 *, 8) << 0x18) >> 0x1C;
    if (temp_r5 == 6) {
        if (temp_r6 == 1) {
            var_r4 = 1;
        }
        else if (temp_r6 == 2) {
            var_r4 = 1;
        }
        else if (temp_r6 == 4) {
            if (temp_r0 == 1) {
                var_r4 = 1;
            }
        }

    }
    return var_r4;
}
