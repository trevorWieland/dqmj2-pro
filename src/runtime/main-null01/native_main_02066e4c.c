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
extern u32 native_fn_020672f4();
extern u8 native_data_021c36e8[];
u32 native_main_02066e4c(void) {
    u32 temp_r0;
    s32 var_r4;
    s32 temp_r5;
    void *var_r6;

    if (M2C_FIELD(native_data_021c36e8, void **, 4) == NULL) {
        return (u32) M2C_FIELD(native_data_021c36e8, void **, 4);
    }
    temp_r5 = M2C_FIELD(M2C_FIELD(native_data_021c36e8, void **, 4), s32 *, 4);
    var_r6 = M2C_FIELD(native_data_021c36e8, void **, 4) + 8;
    var_r4 = 0;
    if ((temp_r5 > 0) && (temp_r5 > 0)) {
        do {
            temp_r0 = native_fn_020672f4(M2C_FIELD(var_r6, u16 *, 6));
            var_r4 += 1;
            var_r6 += 0xA;
        } while (var_r4 < temp_r5);
        return temp_r0;
    }
    return (u32) M2C_FIELD(native_data_021c36e8, void **, 4);
}
