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
extern u32 native_fn_0208ef34();
extern u32 native_fn_0208ef4c();
extern u8 native_data_021d154c[];
u32 native_main_0208ee68(void *arg0, void *arg1) {
    void *var_r6;
    void *temp_r7;
    void *temp_r7_2;

    M2C_FIELD(arg0, s8 *, 0x73) = (s8) M2C_FIELD(arg1, s8 *, 0);
    M2C_FIELD(arg0, s8 *, 0x72) = (s8) M2C_FIELD(arg1, s8 *, 1);
    var_r6 = arg0 + 0x80;
    if (M2C_FIELD(arg1, u16 *, 2) != 0) {
        M2C_FIELD(arg0, void **, 0x64) = var_r6;
        M2C_FIELD(var_r6, u16 *, 0xFC) = (u16) M2C_FIELD(arg1, u16 *, 4);
        temp_r7 = var_r6;
        var_r6 = (void *) native_fn_0208ef34(native_fn_0208ef34(native_fn_0208ef4c(var_r6 + 0x114, var_r6, arg1 + 0x10), arg0 + 0x3C, M2C_FIELD(arg1, u16 *, 2)), arg0 + 0x50, M2C_FIELD(arg1, u16 *, 8));
        M2C_FIELD(temp_r7, u16 *, 0x10A) = (u16) M2C_FIELD(arg1, u16 *, 0xE);
        M2C_FIELD(temp_r7, s32 *, 0x110) = 0;
        M2C_FIELD(temp_r7, s32 *, 0x10C) = (s32) M2C_FIELD(temp_r7, s32 *, 0x110);
    }
    if (M2C_FIELD(arg1, u16 *, 6) != 0) {
        M2C_FIELD(arg0, void **, 0x68) = var_r6;
        M2C_FIELD(var_r6, void **, 0x10C) = arg0;
        temp_r7_2 = var_r6;
        var_r6 = (void *) native_fn_0208ef34(native_fn_0208ef34(native_fn_0208ef34(native_fn_0208ef4c(var_r6 + 0x110, var_r6, arg1 + 0x14), arg0 + 0x48, M2C_FIELD(arg1, u16 *, 6)), arg0 + 0x58, M2C_FIELD(arg1, u16 *, 0xA)), var_r6 + 0xF8, M2C_FIELD(arg1, u16 *, 0xC));
        M2C_FIELD(temp_r7_2, s32 *, 0x108) = 0;
        M2C_FIELD(temp_r7_2, s32 *, 0x104) = (s32) M2C_FIELD(temp_r7_2, s32 *, 0x108);
    } else {
        M2C_FIELD(arg0, void **, 0x68) = (void *) M2C_FIELD(*(u32 *)native_data_021d154c, void **, 0x68);
    }
    return (u32) var_r6;
}
