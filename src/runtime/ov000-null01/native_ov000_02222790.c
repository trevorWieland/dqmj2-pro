#define NULL ((void *)0)
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
extern u32 native_fn_02049ad0();
extern u32 native_fn_0206006c();
extern u32 native_fn_0206b324();
extern u32 native_fn_020851d4();
u32 native_ov000_02222790(s32 arg0) {
    u8 *temp_r0;
    s8 temp_r1;
    void *temp_r2;
    void *temp_r3;
    s8 var_r6;

    native_fn_0206b324(0);
    var_r6 = 0;
    do {
        temp_r0 = native_fn_02049ad0(var_r6);
        temp_r2 = M2C_FIELD(temp_r0, void **, 0);
        if ((temp_r2 != NULL) && (temp_r1 = M2C_FIELD(temp_r0, s8 *, 5), (temp_r1 != 0x7F))) {
            temp_r3 = M2C_FIELD(temp_r2, void **, 4);
            native_fn_0206006c((temp_r1 * 0xC) + arg0, M2C_FIELD(temp_r3, s8 *, 0x5C), M2C_FIELD(temp_r3, s8 *, 0x5D), M2C_FIELD(temp_r3, s8 *, 0x5E), (s32) M2C_FIELD(temp_r3, s8 *, 0x5F));
        }
        var_r6 += 1;
    } while ((s32) var_r6 < 0x24);
    return native_fn_020851d4();
}
