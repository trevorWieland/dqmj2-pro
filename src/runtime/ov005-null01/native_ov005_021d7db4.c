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
extern u32 native_fn_020117c4();
extern u32 native_fn_020126a4();
extern u32 native_fn_ov005_021d773c();
extern u32 native_fn_ov005_021d7778();
extern u32 native_fn_ov005_021d7874();
extern u8 native_data_ov005_021e78c4[];
u32 native_ov005_021d7db4(u16 *arg0) {
    u16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r0_3;
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_data_ov005_021e78c4, void **, 4);
    if (arg0 != NULL) {
        temp_r0_3 = native_fn_ov005_021d7778(temp_r4, arg0);
        if (temp_r0_3 == 0) {
            return temp_r0_3;
        }
    }
    if (arg0 == NULL) {
        M2C_FIELD(temp_r4, s32 *, 0x50F0) = 1;
        return native_fn_ov005_021d773c(temp_r4, 4, native_fn_020126a4(native_ov005_021d7db4));
    }
    temp_r0_2 = *arg0;
    if (temp_r0_2 != 4) {
        return (u32) temp_r0_2;
    }
    temp_r0 = native_fn_ov005_021d773c(temp_r4, 2, native_fn_020117c4());
    if (temp_r0 == 0) {
        return temp_r0;
    }
    M2C_FIELD(native_data_ov005_021e78c4, void **, 4) = NULL;
    return native_fn_ov005_021d7874(temp_r4, 0, 0);
}
