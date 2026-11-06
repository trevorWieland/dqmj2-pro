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
extern u32 native_fn_02065d88();
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021db9f4();
extern u8 native_data_ov001_02238d7c[];
u32 native_ov001_021ea4c4(void) {
    if ((((u32) (M2C_FIELD((void *) native_fn_0207afec(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)), u16 *, 8) << 0x10) >> 0x1C) == 1) || (native_fn_ov001_021db9f4(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60)) != 0) || ((M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD) != 0) && (M2C_FIELD((void *) native_fn_02065d88(), u8 *, 0x2D) == 4) && ((M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36) == 0) || ((u32) (u16) (M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36) + 0xFF35) <= 1U)) && (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x14) == 0))) {
        return 1U;
    }
    return 0U;
}
