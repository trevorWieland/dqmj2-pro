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
extern u32 native_fn_02045dc4();
extern u32 native_fn_02085094();
extern u8 native_data_02102974[];
u32 native_main_02049d50(void) {
    u32 temp_r4;
    void *temp_r4_2;

    temp_r4_2 = M2C_FIELD(native_data_02102974, void **, 0x10);
    if (temp_r4_2 == NULL) {
        return 0U;
    }
    native_fn_02045dc4(1, M2C_FIELD(temp_r4_2, u8 *, 0x30), M2C_FIELD(temp_r4_2, u8 *, 0x1C), M2C_FIELD(temp_r4_2, u8 *, 0x1D), (s32) M2C_FIELD(temp_r4_2, u8 *, 0x1E), (s32) M2C_FIELD(temp_r4_2, u8 *, 0x1F));
    temp_r4 = M2C_FIELD(temp_r4_2, u8 *, 0x1E) * M2C_FIELD(temp_r4_2, u8 *, 0x1F);
    native_fn_02085094(temp_r4_2);
    M2C_FIELD(native_data_02102974, void **, 0x10) = NULL;
    M2C_FIELD(native_data_02102974, s32 *, 0xC) = 0;
    return temp_r4;
}
