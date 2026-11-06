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
extern u32 native_fn_0204b178();
extern u32 native_fn_0205f98c();
extern u32 native_fn_0205fa4c();
extern u8 native_data_ov000_02236a84[];
u32 native_ov000_021ebc80(s32 arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_0205f98c(M2C_FIELD(M2C_FIELD(native_data_ov000_02236a84, void **, 0xC), s32 *, 0x1C), 0);
    switch (arg0) {
    default:
        return temp_r0;
    case 1:
        native_fn_0204b178(temp_r0, 0x34);
        return native_fn_0205fa4c(M2C_FIELD(native_data_ov000_02236a84, void **, 0xC), 1);
    case 0:
        native_fn_0204b178(temp_r0, 0x1F);
        return native_fn_0205fa4c(M2C_FIELD(native_data_ov000_02236a84, void **, 0xC), 1);
    case 2:
        return native_fn_0205fa4c(M2C_FIELD(native_data_ov000_02236a84, void **, 0xC), 0);
    }
}
