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
extern u32 native_fn_02061de4();
extern u32 native_fn_02062a10();
extern u8 native_data_021d6bb4[];
u32 native_main_020d0fe0(u32 arg0) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = native_fn_02061944();
    temp_r0 = native_fn_02062a10(arg0);
    if (temp_r0 != 0) {
        goto block_2;
    }
    return temp_r0;
block_2:
    return native_fn_02061de4(((M2C_FIELD(native_data_021d6bb4, u8 *, 1) + 3) * 0xC) + (temp_r4 + 0x10), M2C_FIELD(temp_r0, s16 *, 0x18), M2C_FIELD(native_data_021d6bb4, u8 *, 1), 1, 0);
}
