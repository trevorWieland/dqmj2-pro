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
extern u32 native_fn_02061944();
extern u32 native_fn_0206de54();
extern u8 native_data_021c4f60[];
extern u8 native_data_021c50e8[];
u32 native_main_02071700(void) {
    M2C_FIELD((void *) native_fn_02061944(), s8 *, 0x26A) = 0;
    native_fn_02008d78(native_data_021c50e8, 0, 0xE4);
    M2C_FIELD(native_data_021c4f60, s8 *, 4) = 0;
    M2C_FIELD(native_data_021c4f60, s8 *, 2) = 6;
    M2C_FIELD(native_data_021c4f60, s32 *, 0x30) = 0;
    return native_fn_0206de54(1);
}
