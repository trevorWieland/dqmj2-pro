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
extern u32 native_fn_02044f9c();
extern u32 native_fn_0207c8a4();
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021e8da0();
u32 native_ov001_021e3b34(void) {
    s32 var_r5;
    u32 temp_r7;
    u32 temp_r7_2;
    void *temp_r1;
    void *temp_r1_2;

    var_r5 = 0;
    do {
        temp_r7 = native_fn_ov001_021db438(0, var_r5);
        if (native_fn_ov001_021db8d0() != 0) {
            temp_r1 = M2C_FIELD(temp_r7, void **, 0x1E8);
            native_fn_0207c8a4(1, native_fn_02044f9c(M2C_FIELD(temp_r1, s16 *, 0x2A), M2C_FIELD(temp_r1, u8 *, 0x2C)));
        }
        temp_r7_2 = native_fn_ov001_021db438(2, var_r5);
        if (native_fn_ov001_021db8d0() != 0) {
            temp_r1_2 = M2C_FIELD(temp_r7_2, void **, 0x1E8);
            native_fn_0207c8a4(1, native_fn_02044f9c(M2C_FIELD(temp_r1_2, s16 *, 0x2A), M2C_FIELD(temp_r1_2, u8 *, 0x2C)));
        }
        var_r5 += 1;
    } while (var_r5 < 3);
    return native_fn_ov001_021e8da0();
}
