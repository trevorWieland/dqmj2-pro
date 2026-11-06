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
extern u32 native_arm7_fn_027e275c(u32, u32);
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_038073a4(u32);
u32 native_arm7_main_027e874c(void *arg0) {
    u8 sp0[512];
    u16 temp_r4;
    void *temp_r0;
    void *temp_r0_2;

    temp_r4 = M2C_FIELD((void *) native_arm7_fn_027e275c((u32) &sp0, (u32) (u16) M2C_FIELD(arg0, s32 *, 4)), u16 *, 4);
    if (temp_r4 != 0) {
        temp_r0_2 = (void *) native_arm7_fn_038073f0();
        M2C_FIELD(temp_r0_2, s16 *, 0) = 0x24;
        M2C_FIELD(temp_r0_2, s16 *, 2) = 1;
        M2C_FIELD(temp_r0_2, s16 *, 4) = 0x242;
        M2C_FIELD(temp_r0_2, u16 *, 6) = temp_r4;
        return native_arm7_fn_038073a4((u32) temp_r0_2);
    }
    temp_r0 = (void *) native_arm7_fn_038073f0();
    M2C_FIELD(temp_r0, s16 *, 0) = 0x24;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_arm7_fn_038073a4((u32) temp_r0);
}
