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
extern u32 native_arm7_fn_037f8d58(u32, u32, u32, u32);
u32 native_arm7_main_027efec8(u32 arg0, void *arg1) {
    u16 temp_r2;
    void *temp_lr;

    temp_lr = arg1 + (M2C_FIELD(arg1, u16 *, 0xE) * 2);
    M2C_FIELD(arg1, u16 *, 0xC) = (u16) M2C_FIELD(temp_lr, u16 *, 0x10);
    M2C_FIELD(temp_lr, s16 *, 0x12) = 2;
    M2C_FIELD(temp_lr, s16 *, 0x14) = 0;
    temp_r2 = M2C_FIELD(arg1, u16 *, 0x18);
    M2C_FIELD(temp_lr, u16 *, 0x16) = temp_r2;
    return native_arm7_fn_037f8d58(arg0, (u32) arg1, (u32) temp_r2, 2U);
}
