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
extern u32 native_fn_0204106c(void *,void *,u32);
extern u32 native_fn_02041268(void *,void *,u32,u32);
extern u32 native_fn_02041448(void *,void *,u32);
extern u32 native_fn_02041474(void *,void *,u32);
extern u8 native_data_02102e2c[];
u32 native_main_0205ca44(void *arg0, s32 arg1) {
    s32 temp_r4;
    u32 var_r5;
    s32 temp_r6;

    temp_r6 = (arg1 * 0xAC) + (s32) native_data_02102e2c;
    temp_r4 = M2C_FIELD(temp_r6, s32 *, 0xC);
    var_r5 = 0;
    if (temp_r4 & 1) {
        var_r5 |= native_fn_0204106c((u8 *)arg0 + 0x14, (void *)(temp_r6 + 0x10), 0);
    }
    if (temp_r4 & 2) {
        var_r5 |= native_fn_02041268((u8 *)arg0 + 0x14, (void *)(temp_r6 + 0x68), 0, 0) * 2;
    }
    if (temp_r4 & 4) {
        var_r5 |= native_fn_02041448((u8 *)arg0 + 0x14, (void *)(temp_r6 + 0x6C), 0) * 4;
    }
    if (temp_r4 & 8) {
        var_r5 |= native_fn_02041474((u8 *)arg0 + 0x14, (void *)(temp_r6 + 0x70), 0) * 8;
    }
    M2C_FIELD(arg0, s32 *, 0x90) = 0x19A;
    M2C_FIELD(arg0, s32 *, 0x94) = 0x19A;
    M2C_FIELD(arg0, s32 *, 0x98) = 0x19A;
    return var_r5;
}
