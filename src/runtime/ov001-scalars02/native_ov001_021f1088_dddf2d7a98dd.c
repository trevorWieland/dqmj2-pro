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
extern u32 native_fn_02048f6c();
extern u32 native_fn_0204b9d0();
extern u32 native_fn_0204baec();
extern u32 native_fn_0204bb08();
extern u32 native_fn_ov001_021f0f60();
extern u32 native_fn_ov001_021f106c();
extern u8 native_data_ov001_02238f6c[];
u32 native_ov001_021f1088(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov001_021f106c();
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_fn_0204b9d0(native_fn_0204baec(), native_data_ov001_02238f6c);
    native_fn_ov001_021f0f60(*(u32 *)(native_data_ov001_02238f6c + (native_fn_02048f6c(0) * 4)));
    return native_fn_0204bb08(0);
}
