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
extern u32 native_fn_02048a60();
extern u32 native_fn_02049ae4();
extern u32 native_fn_0205f98c();
extern u32 native_fn_0205f9e4();
extern u32 native_fn_ov006_021e648c();
extern u8 native_data_ov006_02218e60[];
u32 native_ov006_021e8e5c(u32 arg0, u32 arg1, u32 arg2) {
    u8 *temp_r0;
    void *temp_r5;

    temp_r0 = native_fn_02049ae4();
    if ((temp_r0 != NULL) && (temp_r5 = M2C_FIELD(temp_r0, void **, 4), (temp_r5 != NULL))) {
        native_fn_02048a60(native_fn_0205f98c(M2C_FIELD(native_data_ov006_02218e60, s32 *, 0x1C), 0), 0xE0, (((M2C_FIELD(temp_r5, u8 *, 0x33) + M2C_FIELD(temp_r5, u8 *, 0x35)) - 3) * 8) + 4);
    }
    native_fn_0205f9e4(native_data_ov006_02218e60);
    return native_fn_ov006_021e648c(arg2);
}
