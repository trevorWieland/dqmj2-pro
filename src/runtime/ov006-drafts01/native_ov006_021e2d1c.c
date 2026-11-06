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
extern u32 native_fn_01ff8604();
extern u32 native_fn_0202a164();
extern u32 native_fn_020414c8();
extern u32 native_fn_02041538();
extern u32 native_fn_02041814();
extern u32 native_fn_0205e814();
extern u32 native_fn_020642cc();
extern u32 native_fn_02064488();
extern u32 native_fn_020644c0();
extern u32 native_fn_ov006_021d77d8();
extern u32 native_fn_ov006_021ded5c();
extern u32 native_fn_ov006_021dee68();
extern u32 native_fn_ov006_021def28();
extern u32 native_fn_ov006_021df150();
extern u32 native_fn_ov006_021df590();
extern u32 native_fn_ov006_021e2c8c();
extern u32 native_fn_ov006_021e2ef4();
extern u32 native_fn_ov006_021e2f28();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_ov006_02217bd8;
extern Record_native_data_ov006_02217bd8 native_data_ov006_02217bd8;
u32 native_ov006_021e2d1c(void) {
    u32 var_r4;

    var_r4 = 2;
    switch (native_data_ov006_02217bd8.field_4) {
    default:
        break;
    case 0:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021ded5c(0xF, 0xA, 0xB);
            native_fn_ov006_021def28(1);
            native_fn_ov006_021e2c8c(1);
            native_fn_ov006_021e2ef4();
        }
        break;
    case 1:
        if (native_fn_ov006_021e2f28() == 1) {
            native_fn_ov006_021df590(0x57);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 0xA, 0xC);
            native_fn_ov006_021e2c8c(2);
        }
        break;
    case 2:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021ded5c(0xF, 3, 3);
            native_fn_ov006_021def28(1);
            native_fn_01ff8604(0);
            native_fn_02064488(2);
            native_fn_ov006_021e2c8c(3);
        }
        break;
    case 3:
        if (native_fn_020644c0() != 0) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x57);
            native_fn_ov006_021ded5c(0xF, 3, 4);
            native_fn_ov006_021e2c8c(4);
        }
        break;
    case 4:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_0202a164(7);
            native_fn_ov006_021d77d8(7);
            native_fn_ov006_021e2c8c(5);
            native_fn_020414c8(0x3F);
            native_fn_02041538(1, 2, 0xA);
            native_fn_0205e814(0, 0, 0xA);
            native_fn_020642cc(0);
        }
        break;
    case 5:
        if (native_fn_02041814() != 1) {
            var_r4 = 6;
        }
        break;
    }
    return var_r4;
}
