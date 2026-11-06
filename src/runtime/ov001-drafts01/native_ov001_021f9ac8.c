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
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021dba58();
extern u32 native_fn_ov001_021dbac8();
u32 native_ov001_021f9ac8(void) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_ov001_021dba58(0, 2);
    temp_r4 = native_fn_ov001_021dba58(0, 1);
    if (native_fn_ov001_021dbac8(0) != 0) {
        native_fn_ov001_021d75d4(0x19);
    } else if (temp_r5 != 0) {
        native_fn_ov001_021d75d4(0x17);
    } else if (temp_r4 != 0) {
        native_fn_ov001_021d75d4(0x16);
    } else {
        native_fn_ov001_021d75d4(0x15);
    }
    native_fn_ov001_021d77b0(-1, 0xB4000);
    return native_fn_ov001_021d94cc(1, 0);
}
