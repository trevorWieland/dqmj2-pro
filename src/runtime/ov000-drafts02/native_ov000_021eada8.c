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
extern u8 native_data_ov000_02236950[];
void native_ov000_021eada8(s16 arg0, s8 arg1) {
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F2) = arg0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s8 *, 0x1F5) = arg1;
    M2C_FIELD(native_data_ov000_02236950, s8 *, 5) = 5;
}
