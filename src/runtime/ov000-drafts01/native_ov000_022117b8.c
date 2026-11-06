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
extern u32 native_fn_0201d444();
extern u32 native_fn_02028d50();
extern u8 native_data_ov000_0222f844[];
u32 native_ov000_022117b8(void *arg0) {
    u8 sp0[16];
    s32 var_r6;
    void *temp_r9;

    var_r6 = 0;
    M2C_FIELD(arg0, s32 *, 0x164) = 0;
    do {
        native_fn_0201d444(&sp0, native_data_ov000_0222f844, var_r6);
        temp_r9 = arg0 + var_r6;
        M2C_FIELD(temp_r9, s8 *, 0x150) = (s8) native_fn_02028d50(arg0 + 0x14, &sp0);
        if ((s32) M2C_FIELD(temp_r9, s8 *, 0x150) >= 0) {
            M2C_FIELD(arg0, s32 *, 0x164) = (s32) (M2C_FIELD(arg0, s32 *, 0x164) | (1 << var_r6));
        }
        var_r6 += 1;
    } while (var_r6 < 0x14);
    return 0U;
}
