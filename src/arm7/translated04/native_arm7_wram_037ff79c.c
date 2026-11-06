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
extern u32 native_arm7_fn_037ffeb8(u32, u32);
u32 native_arm7_wram_037ff79c(void *arg0, s32 arg1, u32 arg2) {
    u8 temp_r3;

    temp_r3 = M2C_FIELD(arg0, u8 *, 0);
    if ((u32) temp_r3 < 8U) {
        return 0U;
    }
    if ((u32) temp_r3 > 0xDU) {
        return 0U;
    }
    M2C_FIELD(arg0, s8 *, 1) = 1;
    M2C_FIELD(arg0, s32 *, 0x44) = arg1;
    M2C_FIELD(arg0, s16 *, 0x3C) = 0x1F46;
    native_arm7_fn_037ffeb8((u32) arg0, arg2);
    return 1U;
}
