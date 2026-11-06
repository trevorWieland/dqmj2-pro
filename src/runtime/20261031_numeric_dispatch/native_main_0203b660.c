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
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32 mask);
extern void native_fn_02009264(u32 slot, u32 first, u32 second, void (*callback)(void *), void *context);
extern void native_fn_0200932c(u32 channel, u32 mode, u32 address, u32 repeat, u32 offset, u32 words, u32 volume, u32 zero, u32 scale, u32 pan);
extern u32 native_fn_02026350(u32 numerator, u32 denominator);
extern void native_fn_0202ba20(u8 *view, void *node);
extern u32 native_fn_02038970(void);
extern void native_fn_0203b854(void *context, s32 flag);
extern void native_fn_0203b9b0(void *);
extern void native_fn_0203b9c0(void *context, u32 zero);
extern u8 native_data_020f5b00[];
extern u8 native_data_020f5b4c[];
u32 native_main_0203b660(void *arg0, s32 arg1, s32 arg2, u32 arg3, u32 arg4, u32 arg5, s32 arg6, s32 arg7) {
    u32 quotient;
    u32 temp_r0;
    u32 var_r0;
    u8 temp_r0_2;
    s32 temp_r1;
    u32 temp_r4;
    s32 var_r6;
    u32 sp18;

    temp_r1 = (s32) ((u32)M2C_FIELD(arg0, u32 *, 0x24) << 0x1F) >> 0x1F;
    if (temp_r1 != 0) {
        native_fn_0203b854(arg0, temp_r1);
    }
    quotient = native_fn_02026350(arg3, M2C_FIELD(arg0, s32 *, 0x48) * (arg5 << 5));
    var_r0 = (quotient * arg5) * 32U;
    M2C_FIELD(arg0, u32 *, 0x28) = var_r0;
    if (arg1 == 1) {
        var_r0 = var_r0 >> 1;
    }
    sp18 = native_fn_02026350(arg4 * var_r0, arg5);
    temp_r0 = native_fn_02038970();
    M2C_FIELD(arg0, u32 *, 0x40) = temp_r0;
    if ((s32) temp_r0 < 0) {
        return 0U;
    }
    var_r6 = 0;
    if ((s32) M2C_FIELD(arg0, s32 *, 0x48) > 0) {
        do {
            temp_r0_2 = M2C_FIELD((arg0 + var_r6), u8 *, 0x4C);
            M2C_FIELD((native_data_020f5b4c + (temp_r0_2 * 8)), u32 *, 0) = (M2C_FIELD(arg0, u32 *, 0x28) * var_r6) + arg2;
            M2C_FIELD((native_data_020f5b4c + (temp_r0_2 * 8)), s32 *, 4) = 0;
            native_fn_0200932c(temp_r0_2, arg1, M2C_FIELD((native_data_020f5b4c + (temp_r0_2 * 8)), u32 *, 0), 1, 0, (u32) M2C_FIELD(arg0, u32 *, 0x28) >> 2, 0x7F, 0, arg4 << 5, 0x40);
            var_r6 += 1;
        } while (var_r6 < (s32) M2C_FIELD(arg0, s32 *, 0x48));
    }
    native_fn_02009264(M2C_FIELD(arg0, u32 *, 0x40), sp18, sp18, native_fn_0203b9b0, arg0);
    native_fn_0202ba20(native_data_020f5b00, arg0);
    M2C_FIELD(arg0, s32 *, 0x20) = arg1;
    M2C_FIELD(arg0, s32 *, 0x2C) = arg5;
    M2C_FIELD(arg0, s32 *, 0x30) = arg6;
    M2C_FIELD(arg0, s32 *, 0x34) = arg7;
    M2C_FIELD(arg0, s32 *, 0x38) = 0;
    M2C_FIELD(arg0, s32 *, 0x3C) = 0;
    M2C_FIELD(arg0, s32 *, 0x24) = (s32) ((M2C_FIELD(arg0, s32 *, 0x24) & ~1) | 1);
    temp_r4 = native_fn_02007ff4();
    M2C_FIELD(arg0, s32 *, 0x2C) = 1;
    native_fn_0203b9c0(arg0, 0);
    M2C_FIELD(arg0, s32 *, 0x2C) = arg5;
    native_fn_02008008(temp_r4);
    return 1U;
}
