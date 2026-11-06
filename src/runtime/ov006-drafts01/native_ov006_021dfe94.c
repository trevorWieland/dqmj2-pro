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
extern u32 native_fn_02048f5c();
extern u32 native_fn_02049ad0();
extern u32 native_fn_02049ffc();
extern u8 native_data_ov006_0220d0c0[];
extern u8 native_data_ov006_0220f614[];
u32 native_ov006_021dfe94(s32 arg0) {
    void *temp_r4;

    temp_r4 = native_data_ov006_0220f614 + (arg0 * 0x10);
    if (M2C_FIELD(temp_r4, s32 *, 4) == 1) {
        native_fn_02049ffc(M2C_FIELD(*(void **) native_fn_02049ad0((s8) native_data_ov006_0220d0c0[arg0]), s32 *, 4));
        native_fn_02045dc4(1, native_fn_02048f5c(1), M2C_FIELD(temp_r4, u8 *, 0xC), M2C_FIELD(temp_r4, u8 *, 0xD), (s32) M2C_FIELD(temp_r4, u8 *, 0xE), 2);
    }
    M2C_FIELD(temp_r4, s32 *, 4) = 0;
    M2C_FIELD(temp_r4, s32 *, 0) = 0;
    return 0U;
}
