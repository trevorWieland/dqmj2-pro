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
extern u32 native_fn_020c48d0();
extern u32 native_fn_020c48e8();
extern u32 native_fn_020c48f8();
extern u8 native_data_ov000_02236d98[];
u32 native_ov000_021f1298(void) {
    u32 var_r0;
    u8 temp_r1;

    var_r0 = 0;
    if (M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s8 *, 0x20) == 2) {
        temp_r1 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), u8 *, 0x1922);
        switch (temp_r1) {
        case 1:
            native_fn_020c48d0(9, 5, 0x23);
            native_fn_020c48f8(1);
            native_fn_020c48e8(0x52);
            var_r0 = 1;
            break;
        case 2:
            native_fn_020c48d0(9, 5, 0x24);
            native_fn_020c48f8(1);
            native_fn_020c48e8(0x52);
            var_r0 = 1;
            break;
        }
    }
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), u8 *, 0x1922) = 0U;
    return var_r0;
}
