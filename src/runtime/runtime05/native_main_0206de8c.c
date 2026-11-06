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
extern u32 native_fn_02061944();
extern u32 native_fn_0206df70();
extern u32 native_fn_0206e100();
extern u8 native_data_021c4f60[];
u32 native_main_0206de8c(void) {
    u32 temp_r0;

    temp_r0 = native_fn_02061944();
    if (M2C_FIELD(native_data_021c4f60, s32 *, 0x28) != 0) {
        return temp_r0;
    }
    M2C_FIELD(temp_r0, s32 *, 0x260) = 0x6000;
    native_fn_0206df70();
    native_fn_0206e100();
    M2C_FIELD(native_data_021c4f60, s32 *, 0x28) = 1;
    return (u32) native_data_021c4f60;
}
