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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_020620e8();
extern u8 native_data_ov000_02236d98[];
u32 native_ov000_021f1338(void) {
    s8 var_r4;

    var_r4 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s8 *, 0x20);
    switch (var_r4) {
    default:
        break;
    case 0:
        M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s8 *, 0x191D) = 6;
        M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s32 *, 0x100) = 0;
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 1:
        var_r4 = 0;
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 3:
    case 5:
        var_r4 = 0;
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 2:
        var_r4 = 1;
        native_fn_020620e8(0xA, 1);
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 4:
        var_r4 = 3;
        native_fn_020620e8(0xA, 1);
        native_fn_0205e7a8(-1, 0x53);
        break;
    case 6:
        var_r4 = 5;
        native_fn_020620e8(0xA, 1);
        native_fn_0205e7a8(-1, 0x53);
        break;
    }
    return (u32) var_r4;
}
