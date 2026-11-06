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
extern u32 native_fn_020a00ac();
extern u32 native_fn_020a3d70();
u32 native_main_020a2150(void) {
    s32 sp8;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r5_2;
    u32 temp_r6;
    u32 temp_r7;
    u32 var_r4;

    var_r4 = 0;
    sp8 = 0;
    if ((M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x17) != 0) && (M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x20) != 0)) {
        temp_r5 = native_fn_020a3d70();
        if (M2C_FIELD(temp_r5, s32 *, 0x20) != M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x200)) {
            temp_r5_2 = native_fn_020a3d70();
            temp_r4 = native_fn_020a3d70();
            temp_r6 = native_fn_020a3d70();
            temp_r7 = native_fn_020a3d70();
            var_r4 = native_fn_020a00ac(0xC, M2C_FIELD(temp_r5_2, s32 *, 0x20), M2C_FIELD((temp_r4 + ((M2C_FIELD(temp_r6, u8 *, 0xD) + 1) * 4)), s32 *, 0x24), M2C_FIELD((temp_r7 + ((M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0xD) + 1) * 2)), u16 *, 0xA4), &sp8, 1);
            M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x17) = 0;
            M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x20) = 0;
        }
    }
    return var_r4;
}
