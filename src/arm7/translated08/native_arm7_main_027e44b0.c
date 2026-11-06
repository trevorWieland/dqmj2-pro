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
extern u32 native_arm7_fn_027e4508(u32, u32, u32);
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_038073a4(u32);
u32 native_arm7_main_027e44b0(void *arg0) {
    u16 sp0;
    u16 temp_r4;
    u32 var_r0;
    void *temp_r0;

    temp_r4 = (u16) M2C_FIELD(arg0, s32 *, 4);
    var_r0 = native_arm7_fn_027e4508((u32) arg0, 0U, (u32) &sp0);
    if (var_r0 == 1) {
        temp_r0 = (void *) native_arm7_fn_038073f0();
        M2C_FIELD(temp_r0, s16 *, 0) = 0xD;
        M2C_FIELD(temp_r0, s16 *, 2) = 0;
        M2C_FIELD(temp_r0, u16 *, 8) = temp_r4;
        M2C_FIELD(temp_r0, u16 *, 0xA) = sp0;
        var_r0 = native_arm7_fn_038073a4((u32) temp_r0);
    }
    return var_r0;
}
