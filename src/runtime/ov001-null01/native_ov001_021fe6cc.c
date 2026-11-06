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
extern u32 native_fn_0205ff4c();
extern u32 native_fn_ov001_021fe8d4();
typedef struct {
    u8 unknown_0[0x58];
    s32 field_58;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_021fe6cc(void *arg0) {
    void *temp_r0;
    void *temp_r1;

    temp_r0 = M2C_FIELD(arg0, void **, 0);
    if (temp_r0 != NULL) {
        temp_r1 = M2C_FIELD(temp_r0, void **, 4);
        if (temp_r1 != NULL) {
            if (M2C_FIELD(temp_r1, s32 *, 0x60) != 0) {
                native_data_ov001_02239c10.field_58 = (s32) (native_data_ov001_02239c10.field_58 - ((M2C_FIELD(temp_r1, u8 *, 0x5E) * M2C_FIELD(temp_r1, u8 *, 0x5F)) << 5));
            }
            native_fn_ov001_021fe8d4(arg0);
            native_fn_0205ff4c(M2C_FIELD(arg0, void **, 0));
            M2C_FIELD(arg0, void **, 0) = NULL;
            M2C_FIELD(arg0, s8 *, 6) = -1;
            return -1U;
        }
    }
    return (u32) temp_r0;
}
