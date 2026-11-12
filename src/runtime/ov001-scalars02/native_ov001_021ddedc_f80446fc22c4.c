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
extern u32 ov001_record_is_active_021db8d0();
extern u8 native_data_ov001_02238a08[];
extern u8 native_data_ov001_02238a0c[];
u32 native_ov001_021ddedc(s8 arg0, void *arg1, s32 arg2, s32 arg3) {
    if ((ov001_record_is_active_021db8d0(arg1) != 0) && (M2C_FIELD(arg1, s32 *, 0x33C) & arg2)) {
        *(native_data_ov001_02238a08 + (arg3 * 8)) = arg0;
        *(u32 *)(native_data_ov001_02238a0c + (arg3 * 8)) = arg1;
        return 1U;
    }
    return 0U;
}
