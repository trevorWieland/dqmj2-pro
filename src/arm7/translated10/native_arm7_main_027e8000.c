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
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_038073a4(u32);
extern u32 native_arm7_fn_0380528c(u32, u32, u32);
extern u32 native_arm7_data_027f8884;
u32 native_arm7_main_027e8000(u32 arg0, u32 arg1, u32 arg2) {
    u16 *temp_r4;
    void *temp_r0;
    void *temp_r0_2;

    temp_r4 = M2C_FIELD((u32) &native_arm7_data_027f8884, u16 **, 0x550);
    if (*temp_r4 != 1) {
        temp_r0_2 = (void *) native_arm7_fn_038073f0();
        M2C_FIELD(temp_r0_2, s16 *, 0) = 4;
        M2C_FIELD(temp_r0_2, s16 *, 2) = 3;
        return native_arm7_fn_038073a4((u32) temp_r0_2);
    }
    native_arm7_fn_0380528c(1U, arg1, arg2);
    *temp_r4 = 0;
    temp_r0 = (void *) native_arm7_fn_038073f0();
    M2C_FIELD(temp_r0, s16 *, 0) = 4;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_arm7_fn_038073a4((u32) temp_r0);
}
