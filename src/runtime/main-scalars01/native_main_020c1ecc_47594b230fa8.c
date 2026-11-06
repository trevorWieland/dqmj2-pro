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
extern u32 native_fn_02065730();
extern u32 native_fn_ov000_021f2c54();
extern u8 native_data_021d4c28[];
u32 native_main_020c1ecc(s32 *arg0) {
    s32 temp_r0;
    s32 temp_r0_2;

    if (*(u32 *)native_data_021d4c28 != 0) {
        goto block_2;
    }
    return *(u32 *)native_data_021d4c28;
block_2:
    temp_r0 = *arg0 + native_fn_02065730(*(u32 *)native_data_021d4c28, 3, 1, 0, *arg0);
    *arg0 = temp_r0;
    temp_r0_2 = *arg0 + native_fn_02065730(*(u32 *)native_data_021d4c28 + 0xC, 4, 1, 0, temp_r0);
    *arg0 = temp_r0_2;
    *arg0 += native_fn_02065730(*(u32 *)native_data_021d4c28 + 0x18, 5, 1, 0, temp_r0_2);
    return native_fn_ov000_021f2c54();
}
