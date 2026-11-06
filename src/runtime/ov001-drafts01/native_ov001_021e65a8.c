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
extern u32 native_fn_ov001_021e3764();
extern u32 native_fn_ov001_021e4eb0();
extern u32 native_fn_ov001_021e54a0();
extern u32 native_fn_ov001_021e5638();
extern u32 native_fn_ov001_021e5930();
extern u32 native_fn_ov001_021e5ac8();
extern u32 native_fn_ov001_021e5cf8();
extern u32 native_fn_ov001_021e5e04();
extern u32 native_fn_ov001_021e5f88();
extern u32 native_fn_ov001_021e61e4();
extern u32 native_fn_ov001_021e634c();
extern u32 native_fn_ov001_021e6574();
typedef struct {
    u8 unknown_0[0x16];
    u8 field_16;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e65a8(void) {
    u32 var_r0;
    u32 var_r9;

    var_r0 = 1;
    var_r9 = 0;
    do {
        switch (native_data_ov001_02238cd4.field_16) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_021e3764();
            break;
        case 1:
            var_r0 = native_fn_ov001_021e4eb0();
            break;
        case 2:
            var_r0 = native_fn_ov001_021e5930();
            break;
        case 3:
            var_r0 = native_fn_ov001_021e5ac8();
            break;
        case 4:
            var_r0 = native_fn_ov001_021e5cf8();
            break;
        case 5:
            var_r0 = native_fn_ov001_021e5e04(0);
            break;
        case 6:
            var_r0 = native_fn_ov001_021e5e04(1);
            break;
        case 7:
            var_r0 = native_fn_ov001_021e5638(8);
            break;
        case 8:
            var_r0 = native_fn_ov001_021e5638(9);
            break;
        case 9:
            var_r0 = native_fn_ov001_021e5638(5);
            break;
        case 10:
            var_r0 = native_fn_ov001_021e5f88(0xA);
            break;
        case 11:
            var_r0 = native_fn_ov001_021e5f88(0xB);
            break;
        case 12:
            var_r0 = native_fn_ov001_021e5f88(0xC);
            break;
        case 13:
            var_r0 = native_fn_ov001_021e61e4();
            break;
        case 16:
            var_r0 = native_fn_ov001_021e54a0();
            break;
        case 14:
            var_r0 = native_fn_ov001_021e634c();
            break;
        case 15:
            native_fn_ov001_021e6574();
            var_r0 = 0;
            var_r9 = 2;
            break;
        case 17:
            native_fn_ov001_021e6574();
            var_r0 = 0;
            var_r9 = 1;
            break;
        }
    } while (var_r0 != 0);
    return var_r9;
}
