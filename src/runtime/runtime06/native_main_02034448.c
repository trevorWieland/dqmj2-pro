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
void native_main_02034448(s32 *arg0, void *arg1, s32 arg2) {
    u32 temp_r2;
    void *temp_lr;

    temp_lr = M2C_FIELD(arg1, void **, 8);
    temp_r2 = (((s32) M2C_FIELD(arg1, s32 *, 0) >> 0xC) * M2C_FIELD(temp_lr, u16 *, 6)) + arg2;
    *arg0 = M2C_FIELD((temp_lr + ((temp_r2 >> 5) * 4)), s32 *, 0xC) & (1 << (temp_r2 & 0x1F));
}
