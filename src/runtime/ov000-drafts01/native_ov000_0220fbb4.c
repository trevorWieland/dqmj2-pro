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
extern u32 native_fn_020c56b4();
extern u32 native_fn_ov000_0220f0f0();
extern u32 native_fn_ov000_0220f158();
extern u32 native_fn_ov000_0220f2c0();
extern u32 native_fn_ov000_0220f3dc();
extern u32 native_fn_ov000_0220f59c();
extern u32 native_fn_ov000_0220f6cc();
extern u32 native_fn_ov000_0220f858();
u32 native_ov000_0220fbb4(void *arg0) {
    u8 temp_r0;

    temp_r0 = M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 0xA);
    switch (temp_r0) {
    default:
        break;
    case 0:
        native_fn_ov000_0220f0f0(arg0);
        break;
    case 1:
        native_fn_ov000_0220f158(arg0);
        break;
    case 2:
        native_fn_ov000_0220f2c0(arg0);
        break;
    case 3:
        native_fn_ov000_0220f3dc(arg0);
        break;
    case 4:
        native_fn_ov000_0220f59c(arg0);
        break;
    case 5:
        native_fn_ov000_0220f6cc(arg0);
        break;
    case 6:
        native_fn_ov000_0220f858(arg0);
        break;
    case 8:
        native_fn_ov000_0220f858(arg0);
        break;
    }
    return 0U;
}
