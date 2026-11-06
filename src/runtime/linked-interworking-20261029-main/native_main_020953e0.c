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
extern u32 native_fn_02008c14();
extern u32 native_fn_020946ec();
extern u32 native_fn_02095494();
extern u32 native_fn_020954dc();
extern u32 native_fn_02095630();
extern u32 native_fn_020956a4();
u32 native_main_020953e0(s32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_020946ec(0x10);
    switch (arg0) {
    case 0:
        native_fn_02008c14(0, temp_r4 + 0x300, 0x144);
        M2C_FIELD(temp_r4, u8 *, 0xD10) = (u8) native_fn_02095494(temp_r4);
        break;
    case 1:
        M2C_FIELD(temp_r4, u8 *, 0xD10) = (u8) native_fn_02095630();
        M2C_FIELD(temp_r4, s8 *, 0xD0F) = (s8) native_fn_020956a4(temp_r4);
        break;
    case 2:
        native_fn_02008c14(0, temp_r4 + 0x300, 0x144);
        M2C_FIELD(temp_r4, s8 *, 0xD0F) = 0;
        M2C_FIELD(temp_r4, u8 *, 0xD10) = (u8) native_fn_020954dc(temp_r4);
        break;
    }
    return (u32) M2C_FIELD(temp_r4, u8 *, 0xD10);
}
