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
extern u32 native_fn_02041f34();
extern u32 native_fn_02044cdc();
extern u32 native_fn_ov001_021dd010();
u32 native_ov001_021da480(void *arg0, s32 arg1) {
    u32 var_r1;

    var_r1 = 0;
    if (M2C_FIELD(arg0, u8 *, 0x31C) != 0) {
        native_fn_02041f34(arg0, M2C_FIELD(arg0, s32 *, 0x328), M2C_FIELD(arg0, s32 *, 0x32C), M2C_FIELD(arg0, s32 *, 0x330));
        if ((arg1 != 0) || (native_fn_02044cdc(M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), s16 *, 0x2A)) != 1)) {
            native_fn_ov001_021dd010(arg0, M2C_FIELD(arg0, s32 *, 0x334));
        } else {
            M2C_FIELD(arg0, s32 *, 0x42C) = (s32) M2C_FIELD(arg0, s32 *, 0x334);
            M2C_FIELD(arg0, s8 *, 0x430) = 8;
        }
        var_r1 = 1;
    }
    return var_r1;
}
