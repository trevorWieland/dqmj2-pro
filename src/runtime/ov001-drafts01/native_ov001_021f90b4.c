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
extern u32 native_fn_ov001_021f2698();
extern u32 native_fn_ov001_021f2878();
extern u32 native_fn_ov001_021f2e7c();
extern u32 native_fn_ov001_021f35f0();
extern u32 native_fn_ov001_021f43bc();
extern u32 native_fn_ov001_021f4b34();
extern u32 native_fn_ov001_021f4d20();
extern u32 native_fn_ov001_021f57b0();
extern u32 native_fn_ov001_021f5ea0();
extern u32 native_fn_ov001_021f642c();
extern u32 native_fn_ov001_021f6878();
extern u32 native_fn_ov001_021f7a40();
extern u32 native_fn_ov001_021f7d70();
extern u32 native_fn_ov001_021f8208();
extern u32 native_fn_ov001_021f8ab4();
extern u32 native_fn_ov001_021f8b60();
extern u32 native_fn_ov001_021f8d4c();
extern u32 native_fn_ov001_021f8d5c();
extern u32 native_fn_ov001_021f8d6c();
extern u32 native_fn_ov001_021f8d7c();
extern u32 native_fn_ov001_021f8d8c();
extern u32 native_fn_ov001_021f8d9c();
extern u32 native_fn_ov001_021f8dac();
extern u32 native_fn_ov001_021f8dbc();
extern u32 native_fn_ov001_021f8dcc();
extern u32 native_fn_ov001_021f8e70();
extern u32 native_fn_ov001_021f8fd8();
extern u32 native_fn_ov001_021f9074();
extern u32 native_fn_ov001_021f9090();
typedef struct {
    u8 unknown_0[0x1b];
    u8 field_1b;
} Record_native_data_ov001_0223989c;
extern Record_native_data_ov001_0223989c native_data_ov001_0223989c;
u32 native_ov001_021f90b4(void) {
    u32 var_r0;
    u32 var_r6;

    var_r0 = 1;
    var_r6 = 0;
    do {
        switch (native_data_ov001_0223989c.field_1b) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_021f2698();
            break;
        case 1:
            var_r0 = native_fn_ov001_021f2878();
            break;
        case 2:
            var_r0 = native_fn_ov001_021f2e7c();
            break;
        case 3:
            var_r0 = native_fn_ov001_021f35f0();
            break;
        case 4:
            var_r0 = native_fn_ov001_021f43bc();
            break;
        case 5:
            var_r0 = native_fn_ov001_021f4b34();
            break;
        case 6:
            var_r0 = native_fn_ov001_021f57b0();
            break;
        case 7:
            var_r0 = native_fn_ov001_021f5ea0();
            break;
        case 8:
            var_r0 = native_fn_ov001_021f642c();
            break;
        case 9:
            var_r0 = native_fn_ov001_021f6878();
            break;
        case 10:
            var_r0 = native_fn_ov001_021f7a40();
            break;
        case 11:
            var_r0 = native_fn_ov001_021f4d20();
            break;
        case 12:
            var_r0 = native_fn_ov001_021f7d70();
            break;
        case 13:
            var_r0 = native_fn_ov001_021f8208();
            break;
        case 14:
            var_r0 = native_fn_ov001_021f8ab4();
            break;
        case 15:
            var_r0 = native_fn_ov001_021f8b60();
            break;
        case 16:
            var_r0 = native_fn_ov001_021f8d4c();
            break;
        case 17:
            var_r0 = native_fn_ov001_021f8d5c();
            break;
        case 18:
            var_r0 = native_fn_ov001_021f8d6c();
            break;
        case 19:
            var_r0 = native_fn_ov001_021f8d7c();
            break;
        case 20:
            var_r0 = native_fn_ov001_021f8d8c();
            break;
        case 21:
            var_r0 = native_fn_ov001_021f8d9c();
            break;
        case 22:
            var_r0 = native_fn_ov001_021f8dac();
            break;
        case 23:
            var_r0 = native_fn_ov001_021f8dbc();
            break;
        case 24:
            var_r0 = native_fn_ov001_021f8dcc();
            break;
        case 25:
            var_r0 = native_fn_ov001_021f8e70();
            break;
        case 27:
            var_r0 = native_fn_ov001_021f8fd8();
            break;
        case 26:
            var_r0 = native_fn_ov001_021f9074();
            break;
        case 28:
            var_r0 = native_fn_ov001_021f9090();
            var_r6 = 1;
            break;
        }
    } while (var_r0 != 0);
    return var_r6;
}
