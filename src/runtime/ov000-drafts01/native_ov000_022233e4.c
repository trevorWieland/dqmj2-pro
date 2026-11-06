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
extern u32 native_fn_02002c50();
extern u32 native_fn_02008c58();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_020414c8();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048e8c();
extern u32 native_fn_020642dc();
extern u32 native_fn_ov000_02223748();
extern u32 native_fn_ov000_02223c54();
extern u32 native_fn_ov000_02223c60();
extern u32 native_fn_ov000_02223c6c();
u32 native_ov000_022233e4(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r6;

    temp_r4 = native_fn_ov000_02223c54();
    temp_r5 = native_fn_ov000_02223c60();
    temp_r6 = native_fn_0202a1e0(2U);
    native_fn_02048e74(temp_r5, 7);
    M2C_FIELD(temp_r5, s32 *, 4) = 0;
    M2C_FIELD(temp_r5, s32 *, 0) = 0;
    temp_r0 = native_fn_020642dc();
    switch (temp_r0) {
    default:
        break;
    case 0x2F:
        native_fn_02002c50();
        *(s32 *)0x04001000 |= 0x10000;
        break;
    case 0x1:
    case 0x2:
        M2C_FIELD(temp_r5, s32 *, 0) = 1;
        break;
    case 0x8:
    case 0x9:
    case 0xA:
    case 0xB:
    case 0xC:
    case 0xD:
    case 0xE:
    case 0xF:
        M2C_FIELD(temp_r5, s32 *, 0) = 1;
        break;
    case 0x3:
    case 0x10:
    case 0x11:
    case 0x12:
    case 0x13:
    case 0x14:
    case 0x15:
    case 0x16:
    case 0x17:
    case 0x18:
    case 0x19:
    case 0x1A:
    case 0x1B:
    case 0x33:
        M2C_FIELD(temp_r5, s32 *, 0) = 3;
        break;
    }
    M2C_FIELD(temp_r5, s32 *, 8) = 4;
    M2C_FIELD(temp_r5, s32 *, 0xC) = 4;
    M2C_FIELD(temp_r4, s8 *, 0x5A) = 3;
    native_fn_ov000_02223748();
    native_fn_02048e8c();
    native_fn_ov000_02223c6c();
    native_fn_0202a1e0(temp_r6);
    native_fn_020414c8(0x3F);
    return native_fn_02008c58(0xC0, 0x07000400, 0x400);
}
