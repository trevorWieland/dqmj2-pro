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
extern u32 native_fn_02028dec(u32 header, s32 context);
extern u32 native_fn_0202bf2c(s32 descriptor, u32 index);
extern void native_fn_0202e8b8(u32 object, u32 header, s32 context, u32 flags);
extern void native_fn_0202eacc(u8 *context, u32 object);
u32 native_main_020298c8(void *arg0, s32 *arg1, u32 arg2, u32 arg3) {
    u32 var_r4;
    u32 var_r6;
    u32 temp_r0;
    s32 temp_r8;
    u8 *context;
    context = (u8 *)arg0;

    var_r4 = arg2;
    var_r6 = 0;
    if (M2C_FIELD(context, u8 *, 8) != 0) {
        temp_r0 = native_fn_0202bf2c(*arg1, arg3);
        temp_r8 = M2C_FIELD(context, s32 *, 0x10);
        if (var_r4 == 0) {
            var_r4 = native_fn_02028dec(temp_r0, temp_r8);
            M2C_FIELD(context, u8 *, 0xA) = (u8) (M2C_FIELD(context, u8 *, 0xA) | 8);
        }
        if (var_r4 != 0) {
            native_fn_0202e8b8(var_r4, temp_r0, temp_r8, 0);
            native_fn_0202eacc(context + 0xC, var_r4);
            M2C_FIELD(context, u32 *, 0x6C) = var_r4;
            var_r6 = 1;
        }
    }
    return var_r6;
}
