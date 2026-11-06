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
extern u32 native_fn_02008d78();
extern u32 native_fn_020bad00();
extern u32 native_fn_020c225c();
extern u32 native_fn_020d1f14();
extern u8 native_data_021d7070[];
extern u8 native_data_021d7090[];
u32 native_main_020d1f30(void) {
    u32 temp_r0;

    M2C_FIELD(native_data_021d7070, s32 *, 0x14) = -1;
    M2C_FIELD(native_data_021d7070, s32 *, 8) = 0;
    M2C_FIELD(native_data_021d7070, s32 *, 4) = 0;
    native_fn_02008d78(native_data_021d7090, 0, 8);
    temp_r0 = native_fn_020bad00(0x78, native_data_021d7090, 8, native_fn_020d1f14);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    return native_fn_020c225c(0x30000000);
}
