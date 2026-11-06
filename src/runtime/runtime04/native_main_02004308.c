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
void native_main_02004308(void *arg0, s32 arg1) {
    s32 temp_r2;
    u16 temp_r3;

    temp_r3 = M2C_FIELD(arg0, u16 *, 0);
    temp_r2 = temp_r3 & 0xC0;
    if (arg1 < 0) {
        if (temp_r2 == 0x80) {
            M2C_FIELD(arg0, u16 *, 0) = (u16) ((temp_r3 & ~0xC0) | 0xC0);
        }
        M2C_FIELD(arg0, s16 *, 4) = (s16) (0 - arg1);
        return;
    }
    if (temp_r2 == 0xC0) {
        M2C_FIELD(arg0, u16 *, 0) = (u16) ((temp_r3 & ~0xC0) | 0x80);
    }
    M2C_FIELD(arg0, s16 *, 4) = (s16) arg1;
}
