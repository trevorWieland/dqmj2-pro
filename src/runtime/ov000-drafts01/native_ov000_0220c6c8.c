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
extern u32 native_fn_02042c0c();
extern u32 native_fn_ov000_0221089c();
u32 native_ov000_0220c6c8(void *arg0) {
    s16 temp_ip;
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(arg0, s16 *, 0x27A) == 0) {
        M2C_FIELD(arg0, s32 *, 0x290) = (s32) (M2C_FIELD(arg0, s32 *, 0x74) - 0x1800);
        M2C_FIELD(arg0, s32 *, 0x29C) = (s32) M2C_FIELD(arg0, s32 *, 0x74);
        M2C_FIELD(arg0, s8 *, 0x2C1) = 1;
        native_fn_02042c0c(arg0, 0x1F);
        native_fn_ov000_0221089c(arg0, 1);
    }
    temp_ip = M2C_FIELD(arg0, s16 *, 0x27A);
    M2C_FIELD(arg0, s32 *, 0x74) = (s32) (M2C_FIELD(arg0, s32 *, 0x290) + ((temp_ip * 0x710) - ((s32) (temp_ip * (temp_ip * 0xB2)) >> 1)));
    M2C_FIELD(arg0, s16 *, 0x27A) = (s16) (M2C_FIELD(arg0, s16 *, 0x27A) + 1);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x27A) > 0x10) {
        var_r4 = 1;
        M2C_FIELD(arg0, s8 *, 0x2C1) = 0;
    }
    return var_r4;
}
