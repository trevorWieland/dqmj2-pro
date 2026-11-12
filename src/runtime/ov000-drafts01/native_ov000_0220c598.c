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
extern u32 native_fn_02028158();
extern u32 native_fn_0202818c();
extern u32 native_fn_02042c2c();
extern u32 ov000_saved_world_position_get_021e07b8();
u32 native_ov000_0220c598(s32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_0202818c(arg0 + 0x70, ov000_saved_world_position_get_021e07b8(0));
    return native_fn_02028158(temp_r4 - native_fn_02042c2c(arg0));
}
