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
extern u32 native_fn_02042464();
extern u32 native_fn_ov000_021e5f10();
extern u32 native_fn_ov000_021e5f2c();
u32 native_ov000_021e8334(void *arg0) {
    u32 temp_r0;
    void *temp_r1;

    if (M2C_FIELD(arg0, u8 *, 0x2A8) == 0) {
        native_fn_02042464(arg0, native_fn_ov000_021e5f2c(M2C_FIELD(arg0, u8 *, 0x279)), 1);
        M2C_FIELD(arg0, s16 *, 0x2AC) = 0;
        M2C_FIELD(arg0, u8 *, 0x2A8) = 0xAU;
    }
    if (M2C_FIELD(arg0, u8 *, 0x2A8) == 0xA) {
        temp_r1 = M2C_FIELD(arg0, void **, 0x60);
        if ((s32) M2C_FIELD(temp_r1, s32 *, 0) >= (s32) ((M2C_FIELD(M2C_FIELD(temp_r1, void **, 8), u16 *, 4) << 0xC) - 1)) {
            temp_r0 = native_fn_ov000_021e5f10(M2C_FIELD(arg0, u8 *, 0x279));
            if (temp_r0 != 0xFF) {
                M2C_FIELD(arg0, u8 *, 0x2A8) = 0U;
                M2C_FIELD(arg0, u8 *, 0x279) = (u8) temp_r0;
                return 1U;
            }
        }
    }
    M2C_FIELD(arg0, s16 *, 0x2AC) = (s16) (M2C_FIELD(arg0, s16 *, 0x2AC) + 1);
    return 0U;
}
