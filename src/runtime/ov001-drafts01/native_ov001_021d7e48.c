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
extern u8 native_data_ov001_0222fda1[];
extern u8 native_data_ov001_0222fdbc[];
u32 native_ov001_021d7e48(s32 arg0) {
    s32 temp_r1;

    if (arg0 <= 0x31) {
        temp_r1 = arg0 * 0x78;
        if (*(native_data_ov001_0222fda1 + temp_r1) == 2) {
            return (u32) (native_data_ov001_0222fdbc + temp_r1);
        }
    }
    return 0U;
}
