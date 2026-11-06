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
extern u32 native_fn_02008e0c();
extern u32 native_fn_02094818();
extern u32 native_fn_02096050();
extern u32 native_fn_02096094();
extern u8 native_data_020dc448[];
u32 native_main_02095fc8(void *arg0, void *arg1, void *arg2) {
    u32 temp_r0;
    u8 var_r0;
    s32 temp_r6;

    native_fn_02008e0c(native_data_020dc448, arg2, 0x58);
    M2C_FIELD(arg2, s32 *, 4) = (s32) M2C_FIELD(arg0, s32 *, 0);
    M2C_FIELD(arg2, s32 *, 8) = (s32) M2C_FIELD(arg0, s32 *, 4);
    var_r0 = M2C_FIELD(arg1, u8 *, 0xD0D);
    if ((u32) var_r0 < 6U) {
        temp_r6 = native_fn_02094818() << 8;
        if (M2C_FIELD((arg1 + temp_r6), u8 *, 0xC0) != 0) {
            M2C_FIELD(arg2, s32 *, 0xC) = 0;
            M2C_FIELD(arg2, u32 *, 0x10) = native_fn_02096050(arg1 + temp_r6 + 0xC0);
            M2C_FIELD(arg2, u32 *, 0x14) = native_fn_02096094(M2C_FIELD((arg1 + temp_r6), u8 *, 0xD0));
            M2C_FIELD(arg2, u32 *, 0x18) = native_fn_02096050(arg1 + temp_r6 + 0xC4);
            M2C_FIELD(arg2, u32 *, 0x1C) = native_fn_02096050(arg1 + temp_r6 + 0xC8);
            temp_r0 = native_fn_02096050(arg1 + temp_r6 + 0xCC);
            M2C_FIELD(arg2, u32 *, 0x20) = temp_r0;
            return temp_r0;
        }
        M2C_FIELD(arg2, s32 *, 0xC) = 1;
        var_r0 = 0;
        M2C_FIELD(arg2, u32 *, 0x10) = 0U;
        M2C_FIELD(arg2, u32 *, 0x14) = 0U;
        M2C_FIELD(arg2, u32 *, 0x18) = 0U;
        M2C_FIELD(arg2, u32 *, 0x1C) = 0U;
        M2C_FIELD(arg2, u32 *, 0x20) = 0U;
        
        return (u32) var_r0;
    }
    return (u32) var_r0;
}
