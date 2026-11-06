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
extern u32 native_fn_0202a498();
extern u32 native_fn_0204861c();
extern u32 native_fn_0205f920();
extern u32 native_fn_020cfcf0();
extern u32 native_fn_020d0a48();
extern u8 native_data_021d6b48[];
extern u8 native_data_021d6b54[];
u32 native_main_020cfbdc(void) {
    u8 *temp_r0;
    void *temp_r0_2;
    void *temp_r0_3;
    s32 var_r8;

    native_fn_0205f920(native_fn_020d0a48() + 4, 1, 2);
    temp_r0 = native_fn_020d0a48();
    temp_r0_2 = M2C_FIELD(temp_r0, void **, 0x4C);
    if (temp_r0_2 != NULL) {
        native_fn_0205f920(temp_r0_2, 1, 2);
        native_fn_0202a498(2, M2C_FIELD(temp_r0, void **, 0x4C));
        M2C_FIELD(temp_r0, void **, 0x4C) = NULL;
    }
    native_fn_020cfcf0();
    var_r8 = 0;
    do {
        temp_r0_3 = *(u32 *)(native_data_021d6b54 + (var_r8 * 4));
        if (temp_r0_3 != NULL) {
            native_fn_0204861c(1, M2C_FIELD(temp_r0_3, u8 *, 0x81));
            native_fn_0202a498(2, *(u32 *)(native_data_021d6b54 + (var_r8 * 4)));
            *(u32 *)(native_data_021d6b54 + (var_r8 * 4)) = 0;
        }
        var_r8 += 1;
    } while (var_r8 < 2);
    if (M2C_FIELD(native_data_021d6b48, void **, 8) != NULL) {
        native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 8), u8 *, 0x81));
        native_fn_0202a498(2, M2C_FIELD(native_data_021d6b48, void **, 8));
        M2C_FIELD(native_data_021d6b48, void **, 8) = NULL;
    }
    if (M2C_FIELD(native_data_021d6b48, void **, 4) == NULL) {
        return (u32) M2C_FIELD(native_data_021d6b48, void **, 4);
    }
    native_fn_0204861c(1, M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 4), u8 *, 0x81));
    native_fn_0202a498(2, M2C_FIELD(native_data_021d6b48, void **, 4));
    M2C_FIELD(native_data_021d6b48, void **, 4) = NULL;
    return (u32) native_data_021d6b48;
}
