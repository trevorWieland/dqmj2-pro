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
extern u32 native_fn_02049be4();
extern u32 native_fn_02061dcc();
extern u8 native_data_021b9bd4[];
u32 native_main_02061c1c(u32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, s8 arg5, s8 arg6) {
    u32 temp_r0;

    temp_r0 = native_fn_02061dcc();
    if (arg6 != 0) {
        goto block_2;
    }
    native_fn_02049be4(temp_r0, 0, M2C_FIELD(native_data_021b9bd4, s8 *, 0x268), 0x7F, arg1, arg2, arg3, arg4, (s32) M2C_FIELD(native_data_021b9bd4, s32 *, 0x25C) >> 5, (s32) arg5, 1);
    M2C_FIELD(native_data_021b9bd4, s32 *, 0x25C) = (s32) (M2C_FIELD(native_data_021b9bd4, s32 *, 0x25C) + ((arg3 * arg4) << 5));
    goto block_3;
block_2:
    M2C_FIELD(native_data_021b9bd4, s32 *, 0x260) = (s32) (M2C_FIELD(native_data_021b9bd4, s32 *, 0x260) - ((arg3 * arg4) << 5));
    native_fn_02049be4(temp_r0, 0, M2C_FIELD(native_data_021b9bd4, s8 *, 0x268), 0x7F, arg1, arg2, arg3, arg4, (s32) M2C_FIELD(native_data_021b9bd4, s32 *, 0x260) >> 5, (s32) arg5, 1);
block_3:
    return temp_r0;
}
