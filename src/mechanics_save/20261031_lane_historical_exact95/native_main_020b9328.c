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
extern u32 native_fn_02006b7c(u32);
extern void native_fn_020b90bc(u32);
extern u32 native_fn_020b90ec(u32);
extern u32 native_fn_020b9cf4(void);
extern u8 native_data_021d3028[];
u32 native_main_020b9328(void) {
    s32 temp_r0;

    if (native_fn_020b9cf4() != 0) {
        native_fn_020b90bc(2);
    }
    temp_r0 = M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 4);
    switch (temp_r0) {
    case 1:
        return native_fn_020b90ec(2);
    case 2:
        return native_fn_020b90ec(0);
    default:
        return native_fn_02006b7c(0x64);
    }
}
