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
extern u32 native_fn_02048e74();
extern u32 native_fn_02048fcc();
extern u32 native_fn_02068ae8();
extern u32 native_fn_0206c6c0();
extern u32 native_fn_0207ab08();
extern u32 native_fn_0207ac10();
extern u32 native_fn_0207ca14();
extern u32 native_fn_020bf518();
extern u32 native_fn_ov000_0221d438();
extern u32 native_fn_ov000_02229f68();
extern u32 native_fn_ov000_02229fdc();
extern u32 native_fn_ov000_0222a050();
extern u32 native_fn_ov000_0222a0c4();
extern u32 native_fn_ov000_0222a138();
extern u32 native_fn_ov000_0222a1a8();
extern u8 native_data_ov000_02246090[];
extern u8 native_data_ov000_022460c4[];
extern u8 native_data_ov000_022460d4[];
u32 native_ov000_0221a18c(void) {
    native_fn_02048e74(native_data_ov000_022460c4, 0);
    native_fn_02048fcc(native_data_ov000_022460d4);
    native_fn_02068ae8();
    native_fn_020bf518(1);
    native_fn_ov000_0221d438();
    native_fn_0206c6c0(2);
    native_fn_0207ab08(2);
    native_fn_0207ac10(2);
    native_fn_ov000_02229f68(2);
    native_fn_ov000_02229fdc(2);
    native_fn_ov000_0222a050(2);
    native_fn_ov000_0222a0c4(2);
    native_fn_ov000_0222a138(2);
    native_fn_ov000_0222a1a8(2);
    native_fn_0207ca14(2);
    M2C_FIELD(native_data_ov000_02246090, s32 *, 0x18) = 0;
    M2C_FIELD(native_data_ov000_02246090, s8 *, 6) = 1;
    return (u32) native_data_ov000_02246090;
}
