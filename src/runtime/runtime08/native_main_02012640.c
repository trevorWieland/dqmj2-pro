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
extern u32 native_fn_02011834();
extern u32 native_fn_020118a4();
extern u32 native_fn_020119c0();
extern u32 native_fn_02011a34();
u32 native_main_02012640(u32 arg0, s32 arg1) {
    u32 temp_r0;
    u32 var_r0;
    void *temp_r0_2;

    temp_r0 = native_fn_02011a34(1, 0);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    native_fn_02011834(3, arg0);
    temp_r0_2 = (void *) native_fn_020119c0();
    var_r0 = native_fn_020118a4(3, 4, M2C_FIELD(temp_r0_2, s32 *, 0), M2C_FIELD(temp_r0_2, s32 *, 4), M2C_FIELD(temp_r0_2, s32 *, 0x10), arg1);
    if (var_r0 == 0) {
        var_r0 = 2;
    }
    return var_r0;
}
