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
extern u8 *native_fn_02049ad0(u32 slot);
extern void native_fn_0205ff4c(void *resource);
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
    u32 field_8;
} Record_native_data_021c6c14;
extern Record_native_data_021c6c14 native_data_021c6c14;
u32 native_main_0207f1ec(u32 slot) {
    void *var_r0;
    u8 *temp_r4;

    temp_r4 = native_fn_02049ad0(slot);
    native_data_021c6c14.field_8 = (u32) (native_data_021c6c14.field_8 - 1);
    var_r0 = M2C_FIELD(temp_r4, void **, 0);
    if (var_r0 != NULL) {
        var_r0 = M2C_FIELD(var_r0, void **, 4);
        if (var_r0 != NULL) {
            native_data_021c6c14.field_4 = (u32) (native_data_021c6c14.field_4 - (M2C_FIELD(var_r0, u8 *, 0x1E) * M2C_FIELD(var_r0, u8 *, 0x1F)));
            native_fn_0205ff4c(M2C_FIELD(temp_r4, void **, 0));
            M2C_FIELD(temp_r4, void **, 0) = NULL;
            M2C_FIELD(temp_r4, s8 *, 6) = -1;
            return -1U;
        }
    }
    return (u32) var_r0;
}
