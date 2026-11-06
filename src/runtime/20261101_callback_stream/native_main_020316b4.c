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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_0202e380();
u32 native_main_020316b4(void *arg0) {
    void *temp_r0;
    void *temp_r0_2;
    s32 var_r1;
    u8 temp_r2;
    u8 var_r4;

    if (M2C_FIELD(arg0, u32 (**)(void *), 0x34) != NULL) {
        var_r4 = M2C_FIELD(arg0, u8 *, 0x96);
    } else {
        var_r4 = 0;
    }
    if (var_r4 == 1) {
        M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) & ~0x40);
        M2C_FIELD(arg0, u32 (**)(void *), 0x34)(arg0);
        if (M2C_FIELD(arg0, u32 (**)(void *), 0x34) != NULL) {
            var_r4 = M2C_FIELD(arg0, u8 *, 0x96);
        } else {
            var_r4 = 0;
        }
        var_r1 = M2C_FIELD(arg0, s32 *, 8) & 0x40;
    } else {
        var_r1 = 0;
    }
    if (!(M2C_FIELD(arg0, s32 *, 8) & 0x100) && (var_r1 == 0)) {
        temp_r0_2 = M2C_FIELD(arg0, void **, 0);
        temp_r2 = M2C_FIELD(temp_r0_2, u8 *, 8);
        native_fn_0202e380((u32) (temp_r0_2 + (M2C_FIELD(temp_r0_2, u8 *, 1) | (M2C_FIELD(temp_r0_2, u8 *, 2) << 8) | (M2C_FIELD(temp_r0_2, u8 *, 3) << 0x10) | (M2C_FIELD(temp_r0_2, u8 *, 4) << 0x18))), M2C_FIELD(temp_r0_2, u8 *, 5) | (M2C_FIELD(temp_r0_2, u8 *, 6) << 8) | (M2C_FIELD(temp_r0_2, u8 *, 7) << 0x10) | (temp_r2 << 0x18), (u32) temp_r2);
    }
    if (var_r4 == 3) {
        M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) & ~0x40);
        M2C_FIELD(arg0, u32 (**)(void *), 0x34)(arg0);
    }
    temp_r0 = M2C_FIELD(arg0, void **, 0) + 9;
    M2C_FIELD(arg0, void **, 0) = temp_r0;
    return (u32) temp_r0;
}
