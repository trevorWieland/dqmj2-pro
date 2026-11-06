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
extern u32 native_fn_020b8d44();
extern u32 native_fn_020b8d80();
extern u32 native_fn_020b8da0();
extern u32 native_fn_020b8dc4();
extern u32 native_fn_020b8e40();
extern u8 native_data_021d3020[];
u32 native_main_020b8ccc(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, s32 *, 0) = 0x14;
    M2C_FIELD(arg1, s32 *, 4) = 0x44535359;
    M2C_FIELD(arg1, s32 *, 8) = 0xD5;
    M2C_FIELD(arg1, s32 *, 0xC) = 1;
    M2C_FIELD(arg1, s32 *, 0x10) = arg0;
    M2C_FIELD(*(u32 *)native_data_021d3020, s32 *, 0x30) = 0;
    if ((native_fn_020b8d44(native_fn_020b8e40) != 0) && (native_fn_020b8dc4(arg1) != 0)) {
        native_fn_020b8d80();
    }
    return native_fn_020b8da0();
}
