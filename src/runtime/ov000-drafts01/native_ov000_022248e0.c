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
extern u32 native_fn_01ffa5ac();
extern u32 native_fn_01ffb500();
extern u32 native_fn_020894bc();
extern u32 native_fn_020894d4();
typedef struct {
    u8 unknown_0[0x1c];
    s32 field_1c;
    u16 field_20;
    u8 unknown_22[0x3];
    s8 field_25;
} Record_native_data_ov000_02246720;
extern Record_native_data_ov000_02246720 native_data_ov000_02246720;
extern u8 native_data_ov000_0224673c[];
u32 native_ov000_022248e0(void) {
    native_data_ov000_02246720.field_1c = (s32) *(s32 *) native_fn_020894bc();
    native_data_ov000_02246720.field_20 = (u16) *(u16 *) native_fn_01ffb500();
    native_data_ov000_02246720.field_25 = (s8) *(s32 *) native_fn_020894d4();
    return native_fn_01ffa5ac(native_data_ov000_0224673c, 0xC, 5);
}
