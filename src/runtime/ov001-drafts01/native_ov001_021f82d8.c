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
extern u32 native_fn_02041f74();
extern u32 native_fn_02042c2c();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d7814();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021db9e0();
extern u32 native_fn_ov001_021dbaac();
u32 native_ov001_021f82d8(void *arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_ov001_021db9e0();
    if (native_fn_ov001_021dbaac(arg0) != 0) {
        if (M2C_FIELD(arg0, u8 *, 0x31E) == 0) {
            native_fn_ov001_021d75d4(0x12);
        } else {
            native_fn_ov001_021d75d4(0x11);
        }
    } else if (temp_r4 == 2) {
        native_fn_ov001_021d75d4(0x10);
    } else if (temp_r4 == 1) {
        native_fn_ov001_021d75d4(0xF);
    } else {
        native_fn_ov001_021d75d4(0xE);
    }
    native_fn_ov001_021d77b0(-1, native_fn_02042c2c(arg0));
    native_fn_ov001_021d7814(-1, native_fn_02041f74(arg0, 0));
    if (M2C_FIELD(arg0, u8 *, 0x31E) == 0) {
        return native_fn_ov001_021d94cc(1, 0);
    }
    return native_fn_ov001_021d94cc(0, 1);
}
