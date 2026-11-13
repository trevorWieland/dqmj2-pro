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
extern u32 native_fn_0202818c();
extern u32 native_fn_0202859c();
extern u32 native_fn_020285c8();
extern u32 native_fn_0205eb58();
extern u32 ov000_saved_world_position_get_021e07b8();
u32 native_ov000_021e3028(void) {
    u32 temp_r4;
    u32 temp_r4_2;

    temp_r4_2 = native_fn_020285c8(0, 0);
    temp_r4 = native_fn_0202818c(native_fn_0202859c(0, 0), temp_r4_2);
    return native_fn_0205eb58(ov000_saved_world_position_get_021e07b8(0), temp_r4);
}
