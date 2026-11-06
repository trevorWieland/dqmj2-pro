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
extern u32 native_fn_020062f8();
extern u32 native_fn_02006924();
u32 native_main_0200716c(void *arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    void *temp_r0_3;

    temp_r0_2 = M2C_FIELD(arg0, u32 *, 0x88);
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    do {
        temp_r0_3 = (void *) native_fn_020062f8(arg0 + 0x88);
        M2C_FIELD(temp_r0_3, s32 *, 0xC) = 0;
        M2C_FIELD(temp_r0_3, s32 *, 8) = 0;
        native_fn_02006924();
        temp_r0 = M2C_FIELD(arg0, u32 *, 0x88);
    } while (temp_r0 != 0);
    return temp_r0;
}
