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
extern u32 native_fn_020620b4();
extern u32 native_fn_02062358();
extern u32 native_fn_0206a06c();
extern u32 native_fn_ov000_021eadd0();
extern u32 native_fn_ov000_0221a9e4();
extern u32 native_fn_ov000_0221c000();
extern u32 native_fn_ov000_0221cab0();
extern u32 native_fn_ov000_0221d8e0();
extern u32 native_fn_ov000_0221e7e8();
extern u32 native_fn_ov000_0221ed54();
extern u32 native_fn_ov000_0221fc6c();
extern u32 native_fn_ov000_022202b0();
extern u32 native_fn_ov000_022208d0();
extern u32 native_fn_ov000_02221154();
typedef struct {
    u8 unknown_0[0x7];
    s8 field_7;
    u8 unknown_8[0x18];
    s32 field_20;
} Record_native_data_ov000_02246090;
extern Record_native_data_ov000_02246090 native_data_ov000_02246090;
extern u8 native_data_ov000_022460d4[];
u32 native_ov000_0221bb00(s32 *arg0) {
    s8 var_r4;

    var_r4 = M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10);
    *arg0 = 0;
    switch (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10)) {
    default:
        break;
    case 0:
        native_fn_0205e7a8(-1, 0x53);
        native_data_ov000_02246090.field_7 = 8;
        native_fn_ov000_021eadd0();
        break;
    case 1:
        native_fn_0205e7a8(-1, 0x53);
        if (native_fn_ov000_022208d0(native_data_ov000_022460d4, native_data_ov000_02246090.field_20) != 0) {
            var_r4 = 0;
            native_fn_ov000_0221e7e8(0);
        } else {
            native_fn_ov000_0221d8e0();
            native_fn_ov000_0221a9e4();
        }
        break;
    case 2:
        native_fn_ov000_0221fc6c(native_data_ov000_02246090.field_20);
        native_fn_ov000_02221154(native_data_ov000_022460d4, 0, native_data_ov000_02246090.field_20);
        native_fn_ov000_0221cab0();
        native_fn_0205e7a8(-1, 0x53);
        native_fn_ov000_0221e7e8(0);
        var_r4 = 1;
        break;
    case 3:
        native_fn_ov000_022202b0();
        native_fn_ov000_02221154(native_data_ov000_022460d4, 0, native_data_ov000_02246090.field_20);
        native_fn_ov000_0221cab0();
        native_fn_ov000_0221e7e8(0);
        native_fn_0205e7a8(-1, 0x53);
        var_r4 = 1;
        break;
    case 5:
        native_fn_0205e7a8(-1, 0x53);
        var_r4 = 1;
        native_fn_020620b4(1);
        native_fn_02062358(1);
        break;
    case 8:
        if (native_fn_ov000_0221ed54(native_data_ov000_022460d4, 1) != 0) {
            var_r4 = 1;
        }
        *arg0 = 1;
        break;
    case 9:
        native_fn_0205e7a8(-1, 0x53);
        var_r4 = 8;
        break;
    case 10:
        native_fn_0206a06c(1);
        native_fn_ov000_0221c000(1);
        break;
    case 11:
        native_fn_0205e7a8(-1, 0x53);
        native_data_ov000_02246090.field_7 = 8;
        native_fn_ov000_021eadd0();
        break;
    }
    return (u32) var_r4;
}
