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
extern u32 native_fn_ov001_021e9da4();
extern u32 native_fn_ov001_021ea56c();
extern u32 native_fn_ov001_021eaac0();
extern u32 native_fn_ov001_021eabac();
extern u32 native_fn_ov001_021eacb0();
extern u32 native_fn_ov001_021eae04();
extern u32 native_fn_ov001_021eb200();
extern u32 native_fn_ov001_021eb97c();
extern u32 native_fn_ov001_021ebecc();
extern u32 native_fn_ov001_021ec6c0();
extern u32 native_fn_ov001_021ecdb8();
extern u32 native_fn_ov001_021ececc();
extern u32 native_fn_ov001_021ed840();
extern u32 native_fn_ov001_021ed868();
extern u32 native_fn_ov001_021ed8c0();
extern u32 native_fn_ov001_021edcdc();
extern u32 native_fn_ov001_021ede48();
extern u32 native_fn_ov001_021ede58();
extern u32 native_fn_ov001_021ede68();
extern u32 native_fn_ov001_021edf1c();
extern u32 native_fn_ov001_021ee3e0();
typedef struct {
    u8 unknown_0[0x13];
    u8 field_13;
    u8 unknown_14[0x22];
    u16 field_36;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
u32 native_ov001_021ee410(void) {
    u32 var_r0;
    u32 var_r6;

    var_r0 = 1;
    var_r6 = 0;
    do {
        switch (native_data_ov001_02238d7c.field_13) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_021ea56c();
            break;
        case 1:
            var_r0 = native_fn_ov001_021eabac();
            break;
        case 2:
            var_r0 = native_fn_ov001_021eacb0();
            break;
        case 3:
            var_r0 = native_fn_ov001_021eae04();
            break;
        case 5:
            var_r0 = native_fn_ov001_021eb200();
            break;
        case 6:
            var_r0 = native_fn_ov001_021eb97c();
            break;
        case 7:
            var_r0 = native_fn_ov001_021ebecc();
            break;
        case 8:
            var_r0 = native_fn_ov001_021ec6c0();
            break;
        case 9:
            var_r0 = native_fn_ov001_021ecdb8();
            break;
        case 10:
            var_r0 = native_fn_ov001_021ececc();
            break;
        case 11:
            var_r0 = native_fn_ov001_021ed840();
            break;
        case 12:
            var_r0 = native_fn_ov001_021ed868();
            break;
        case 13:
            var_r0 = native_fn_ov001_021ed8c0();
            break;
        case 14:
            var_r0 = native_fn_ov001_021edcdc();
            break;
        case 15:
            var_r0 = native_fn_ov001_021ede48();
            break;
        case 16:
            var_r0 = native_fn_ov001_021ede58();
            break;
        case 17:
            var_r0 = native_fn_ov001_021ede68();
            break;
        case 18:
            var_r0 = native_fn_ov001_021edf1c();
            break;
        case 19:
            var_r0 = native_fn_ov001_021ee3e0();
            var_r6 = 1;
            break;
        }
    } while (var_r0 != 0);
    native_fn_ov001_021e9da4();
    native_fn_ov001_021eaac0(native_data_ov001_02238d7c.field_36);
    return var_r6;
}
