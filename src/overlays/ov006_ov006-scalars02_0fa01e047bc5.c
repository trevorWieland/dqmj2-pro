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
extern u32 native_fn_ov006_02203314();
extern u32 native_fn_ov006_0220490c();
extern u8 native_data_ov006_0221c180[];
u32 native_ov006_022032e0(s16 arg0) {
    void *temp_r4;

    temp_r4 = *(u32 *)native_data_ov006_0221c180;
    if (M2C_FIELD(temp_r4, u8 *, 9) != 0) {
        return 0U;
    }
    M2C_FIELD(temp_r4, u32 *, 0) = native_fn_ov006_0220490c(1, native_fn_ov006_02203314, temp_r4, 0xC8);
    M2C_FIELD(temp_r4, s16 *, 4) = 0;
    M2C_FIELD(temp_r4, s16 *, 6) = arg0;
    M2C_FIELD(temp_r4, s8 *, 9) = 1;
    return 1U;
}
