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
extern u32 native_fn_0202a498();
extern u32 native_fn_020675d8();
extern u32 native_fn_020c1eb0();
extern u32 native_fn_020c49e8();
extern u32 native_fn_020d34fc();
extern u32 native_fn_ov000_021f33a0();
extern u32 native_fn_ov000_021f34ac();
extern u8 native_data_ov000_02236d98[];
u32 native_ov000_021f2474(void) {
    native_fn_020d34fc();
    native_fn_ov000_021f34ac(2);
    native_fn_020c1eb0();
    native_fn_ov000_021f33a0();
    native_fn_020c49e8();
    native_fn_020675d8(2);
    native_fn_0202a498(2, M2C_FIELD(native_data_ov000_02236d98, s32 *, 8));
    M2C_FIELD(native_data_ov000_02236d98, s32 *, 8) = 0;
    return (u32) native_data_ov000_02236d98;
}
