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
extern u32 native_fn_0206db90();
extern u8 native_data_ov000_02236ca3[];
u32 native_ov000_021f03e8(void *arg0) {
    u32 temp_r0;
    void *temp_r4;

    temp_r4 = M2C_FIELD(M2C_FIELD(arg0, void **, 0), void **, 4);
    temp_r0 = native_fn_0206db90(M2C_FIELD(arg0, s8 *, 5));
    if (temp_r0 == 0x7F) {
        return temp_r0;
    }
    return native_fn_02045dc4(1, *(native_data_ov000_02236ca3 + (temp_r0 * 0xC)), M2C_FIELD(temp_r4, u8 *, 0x5C), M2C_FIELD(temp_r4, u8 *, 0x5D), (s32) M2C_FIELD(temp_r4, u8 *, 0x5E), (s32) M2C_FIELD(temp_r4, u8 *, 0x5F));
}
