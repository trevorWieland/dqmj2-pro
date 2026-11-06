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
extern u32 native_fn_ov000_022174a8();
extern u8 native_data_ov000_022455e6[];
extern u8 native_data_ov000_022455e7[];
u32 native_ov000_022167dc(void *arg0) {
    s32 temp_r3;
    u32 temp_r0;
    void *temp_r4;

    temp_r4 = M2C_FIELD(M2C_FIELD(arg0, void **, 0), void **, 4);
    temp_r0 = native_fn_ov000_022174a8(M2C_FIELD(arg0, s8 *, 5));
    if (temp_r0 == 0x7F) {
        return temp_r0;
    }
    temp_r3 = temp_r0 * 0xC;
    return native_fn_02045dc4(*(native_data_ov000_022455e6 + temp_r3), *(native_data_ov000_022455e7 + temp_r3), M2C_FIELD(temp_r4, u8 *, 0x1C), M2C_FIELD(temp_r4, u8 *, 0x1D), (s32) M2C_FIELD(temp_r4, u8 *, 0x1E), (s32) M2C_FIELD(temp_r4, u8 *, 0x1F));
}
