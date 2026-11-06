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
extern u32 native_fn_02048094();
extern u32 native_fn_020653d0();
extern u32 native_fn_020bef78();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0e9c();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u8 native_data_ov005_021e7764[];
extern u8 native_data_ov005_021ed438[];
u32 native_ov005_021e32b8(void) {
    if (((native_fn_020653d0() == 0) || (native_fn_020653d0() == 3)) && (native_fn_020bef78() != 4) && (native_fn_ov005_021e0e9c(M2C_FIELD(M2C_FIELD(native_data_ov005_021ed438, void **, 0x40), s32 *, 0x44)) == 1)) {
        native_fn_ov005_021e1048(0x52);
        native_fn_02048094(M2C_FIELD(M2C_FIELD(native_data_ov005_021ed438, void **, 0x40), s32 *, 0x44), 0);
        native_fn_ov005_021e0730(0x13, 2, 8);
        return native_fn_ov005_021e155c(0x1F);
    }
    *(u32 *)native_data_ov005_021e7764 = -1;
    return native_fn_ov005_021e155c(0x1D);
}
