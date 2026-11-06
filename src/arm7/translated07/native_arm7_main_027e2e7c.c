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
u32 native_arm7_main_027e2e7c(s16 arg0, s16 arg1) {
    void *temp_r0;

    temp_r0 = (void *) native_arm7_fn_038073f0();
    M2C_FIELD(temp_r0, s16 *, 0) = 1;
    M2C_FIELD(temp_r0, s16 *, 2) = 1;
    M2C_FIELD(temp_r0, s16 *, 4) = arg0;
    M2C_FIELD(temp_r0, s16 *, 6) = arg1;
    return native_arm7_fn_038073a4((u32) temp_r0);
}
