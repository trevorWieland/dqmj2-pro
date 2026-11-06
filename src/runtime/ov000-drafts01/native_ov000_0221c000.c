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
extern u32 native_fn_02062a10();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_02072f48();
extern u32 native_fn_ov000_021ead88();
extern u32 native_fn_ov000_021eae04();
extern u32 native_fn_ov000_021eae18();
extern u32 native_fn_ov000_021eb030();
extern u8 native_data_ov000_02246090[];
u32 native_ov000_0221c000(s32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_02062a10(M2C_FIELD(native_data_ov000_02246090, s32 *, 0x2C));
    native_fn_0206dcd0();
    if (temp_r4 != 0) {
        if (native_fn_02072f48(M2C_FIELD(temp_r4, s16 *, 0x18)) == 0) {
            native_fn_ov000_021ead88(M2C_FIELD(temp_r4, s16 *, 0x18), M2C_FIELD(temp_r4, u8 *, 0x1A));
        } else {
            native_fn_ov000_021ead88(0x159, 0U);
        }
    } else {
        native_fn_ov000_021ead88(0, 0U);
    }
    if (arg0 != 0) {
        if (M2C_FIELD(native_data_ov000_02246090, s32 *, 0x2C) == M2C_FIELD(native_data_ov000_02246090, s32 *, 0xC)) {
            native_fn_ov000_021eae04();
        } else {
            native_fn_ov000_021eb030();
            native_fn_ov000_021eae18();
        }
    }
    M2C_FIELD(native_data_ov000_02246090, s8 *, 4) = 0;
    M2C_FIELD(native_data_ov000_02246090, s32 *, 0x10) = (s32) M2C_FIELD(native_data_ov000_02246090, s32 *, 0x2C);
    return (u32) native_data_ov000_02246090;
}
