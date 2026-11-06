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
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b058();
extern u32 native_fn_0207d624();
extern u32 native_fn_0207d6c4();
extern u32 native_fn_ov001_021dc9d4();
extern u32 native_fn_ov001_0220eb88();
extern u32 native_fn_ov001_0220eca8();
extern u32 native_fn_ov001_0220fd80();
extern u8 native_data_ov001_02238d7c[];
u32 native_ov001_021ecdb8(void) {
    if (((M2C_FIELD((void *) native_fn_0207afec(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)), u8 *, 0x21) != 0) || (native_fn_ov001_0220eb88(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s32 *, 0x1E8) + 0x46) != 0) || ((native_fn_0207d6c4(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD)) != 0) && (native_fn_0207b058(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), 0x40) != 0)) || (native_fn_ov001_0220fd80(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)) != 0) || ((native_fn_0207d624(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD)) != 0) && (native_fn_0207b058(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), 0x10) != 0)) || (native_fn_ov001_0220eca8(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s32 *, 0x1E8) + 0x46, M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)) != 0)) && (native_fn_ov001_021dc9d4(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60)) != 0) && (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x14) == 0)) {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 0xA;
    } else {
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 0x11;
    }
    return 1U;
}
