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
extern u32 native_fn_0202a498(u32, u32);
extern u32 native_fn_0204861c();
extern u32 native_fn_0205f98c();
void native_main_0205f920(void *arg0, u32 arg1, u32 arg2) {
    u8 var_r5;
    u32 currentBuffer;

    var_r5 = 0;
    if ((u32) M2C_FIELD(arg0, u8 *, 0x22) <= (u32)var_r5) {
        goto block_2;
    }
loop_1:
    native_fn_0204861c(arg1, M2C_FIELD((void *) native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), var_r5), u8 *, 0x81));
    var_r5 += 1;
    if ((u32) var_r5 < (u32) M2C_FIELD(arg0, u8 *, 0x22)) {
        goto loop_1;
    }
block_2:
    currentBuffer = M2C_FIELD(arg0, u32 *, 0x1C);
    if (currentBuffer != 0) {
        goto block_4;
    }
    return;
block_4:
    native_fn_0202a498(arg2, currentBuffer);
    M2C_FIELD(arg0, s32 *, 0x1C) = 0;
    return;
}
