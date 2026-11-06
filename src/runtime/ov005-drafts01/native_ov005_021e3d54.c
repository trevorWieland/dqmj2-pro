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
extern u32 native_fn_020644c0();
extern u32 native_fn_020bf330();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e5d40();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x4];
    s8 field_9;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
extern u8 native_data_ov005_021edaf4[];
u32 native_ov005_021e3d54(void) {
    u32 temp_r0;

    temp_r0 = native_fn_020644c0();
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_fn_01ff8604(1);
    native_fn_ov005_021e5d40();
    native_fn_ov005_021e0818();
    native_fn_ov005_021e1048(0x57);
    native_data_ov005_021ed438.field_9 = 0;
    native_fn_020bf330(native_data_ov005_021ed438.field_4, native_data_ov005_021edaf4);
    return native_fn_ov005_021e155c(0x2B);
}
