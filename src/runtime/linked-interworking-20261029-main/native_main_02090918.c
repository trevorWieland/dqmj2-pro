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
extern u32 native_fn_0200708c();
extern u32 native_fn_02007110();
extern u32 native_fn_02092bcc();
u32 native_main_02090918(void *arg0) {
    s32 temp_r0;
    void *temp_r4;
    void *temp_r5;
    void *temp_r6;

    temp_r4 = M2C_FIELD(arg0, void **, 4);
    temp_r6 = M2C_FIELD(temp_r4, void **, 0x64);
    temp_r5 = M2C_FIELD(temp_r6, void **, 0xC4);
    native_fn_0200708c(temp_r6 + 0xE0);
    temp_r0 = M2C_FIELD(arg0, s32 *, 0x10);
    if (temp_r0 != 0) {
        M2C_FIELD(temp_r5, s32 *, 0xC) = temp_r0;
        native_fn_02092bcc(1);
        M2C_FIELD(temp_r4, s8 *, 0x73) = 4;
    } else {
        M2C_FIELD(temp_r4, s8 *, 0x73) = 0;
        native_fn_02092bcc();
        M2C_FIELD(temp_r5, s32 *, 0xC) = 0;
    }
    native_fn_02007110(temp_r6 + 0xE0);
    return 0U;
}
