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
extern u32 native_fn_0202ac4c();
extern u32 native_fn_0203d318();
extern u32 native_fn_0203d32c();
extern u32 native_fn_0203d340();
extern u32 native_fn_02066d10();
extern u32 native_fn_02066ee0();
extern u32 native_fn_ov000_021d90f0();
extern u32 native_fn_ov000_021d95a0();
extern u32 native_fn_ov000_021d9af4();
extern u32 native_fn_ov000_021da470();
extern u32 native_fn_ov000_021dd4f8();
extern u32 native_fn_ov000_021dea64();
extern u32 native_fn_ov000_021e4380();
extern u32 native_fn_ov000_021e4db8();
extern u32 native_fn_ov000_021e7290();
extern u32 native_fn_ov000_021e889c();
extern u32 native_fn_ov000_02210968();
extern u32 native_fn_ov000_02212180();
extern u32 native_fn_ov000_022138d8();
extern u8 native_data_020f6054[];
extern u8 native_data_020f60a8[];
void native_main_0203fcec(void) {
    native_fn_ov000_02212180();
    native_fn_ov000_021e4380();
    native_fn_ov000_022138d8();
    native_fn_ov000_02210968();
    native_fn_ov000_021e7290();
    native_fn_ov000_021e889c();
    native_fn_ov000_021d9af4();
    native_fn_ov000_021dea64();
    native_fn_ov000_021dd4f8();
    native_fn_ov000_021da470();
    native_fn_ov000_021e4db8();
    native_fn_ov000_021d95a0();
    native_fn_ov000_021d90f0();
    native_fn_02066ee0();
    native_fn_02066d10();
    native_fn_0202ac4c(native_data_020f60a8);
    native_fn_0203d318();
    native_fn_0203d32c();
    native_fn_0203d340();
    switch (M2C_FIELD(native_data_020f6054, s8 *, 8)) {
    case 1:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0xD;
        return;
    case 0:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 6;
        return;
    case 9:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 7;
        return;
    case 11:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 8;
        return;
    case 10:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 9;
        return;
    case 4:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0xE;
        return;
    case 2:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0xF;
        return;
    case 6:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x10;
        return;
    case 5:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x11;
        return;
    case 12:
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x33;
        return;
    case 3:
    case 7:
    case 8:
        return;

default:
        return;
    }
}
