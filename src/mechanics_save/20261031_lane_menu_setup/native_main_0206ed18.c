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
extern u32 native_fn_02045ed0(u32 arg0);
extern u32 native_fn_02049f4c(void **);
extern u32 native_fn_02061944(void);
extern u32 native_fn_02061c1c(u32 arg0, u32 arg1, u32 arg2, u32 arg3, u32 arg4, u32 arg5, u32 arg6);
extern u32 native_fn_02061dcc(s32);
extern u32 native_fn_0206de8c(void);
extern u32 native_fn_0206efe8(s8);
extern u32 native_fn_0206f070(s8);
u32 native_main_0206ed18(void) {
    s32 var_r4;
    s8 temp_r0;
    s32 temp_r5;

    temp_r0 = M2C_FIELD((void *) native_fn_02061944(), s8 *, 0x26D);
    switch (temp_r0) {
    default:
        break;
    case 0:
    case 8:
    case 9:
    case 10:
    case 14:
    case 16:
    case 19:
    case 27:
    case 28:
    case 29:
    case 30:
    case 32:
    case 34:
    case 35:
    case 36:
    case 37:
    case 38:
    case 42:
        native_fn_0206de8c();
        break;
    }
    native_fn_02061c1c(6U, 2U, 8U, 5U, 2U, 0U, 0U);
    native_fn_02061c1c(7U, 2U, 0xAU, 0xCU, 2U, 1U, 0U);
    native_fn_02061c1c(8U, 2U, 0xCU, 0xCU, 2U, 1U, 0U);
    native_fn_02061c1c(9U, 2U, 0x10U, 0x14U, 2U, 0U, 0U);
    native_fn_02061c1c(0xAU, 0x11U, 8U, 0xAU, 2U, 0U, 0U);
    native_fn_02061c1c(0xBU, 0x11U, 0xAU, 0xAU, 2U, 0U, 0U);
    native_fn_02061c1c(0xCU, 0x11U, 0xCU, 0xAU, 2U, 0U, 0U);
    native_fn_02061c1c(0xDU, 0x11U, 0xEU, 0xAU, 2U, 0U, 0U);
    native_fn_02061c1c(0xEU, 2U, 0x13U, 0xCU, 2U, 0U, 0U);
    native_fn_02061c1c(0xFU, 2U, 0x15U, 0x18U, 2U, 0U, 0U);
    var_r4 = 6;
    do {
        native_fn_02049f4c((void **) native_fn_02061dcc(var_r4));
        temp_r5 = var_r4 + 6;
        native_fn_0206efe8(temp_r5);
        native_fn_0206f070(temp_r5);
        var_r4 = (s32) (s8) (var_r4 + 1);
    } while (var_r4 < 0xA);
    return native_fn_02045ed0(1U);
}
