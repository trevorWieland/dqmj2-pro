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
extern u32 native_fn_0207b058();
extern u32 native_fn_0207d624();
extern u32 native_fn_0207d650();
extern u32 native_fn_ov001_021d908c();
extern u32 native_fn_ov001_021ecc14();
extern u32 native_fn_ov001_02209490();
extern u8 native_data_ov001_02238d7c[];
u32 native_ov001_021ecc48(void) {
    u32 temp_r4;

    temp_r4 = native_fn_ov001_021ecc14(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54), u8 *, 0x31E), 3, 8);
    if ((native_fn_0207d624(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD)) != 0) && (native_fn_0207b058(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), 0x10) != 0) && (native_fn_0207d650(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD), native_fn_ov001_021d908c(temp_r4, M2C_FIELD(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54), void **, 0x1E8), u8 *, 0x8F), native_fn_ov001_02209490(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54) + 0x22C))) != 0)) {
        return 1U;
    }
    return 0U;
}
