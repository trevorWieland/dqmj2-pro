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
#define NULL ((void *)0)
extern u32 native_fn_0203a01c(void *,u32,u32);
extern u32 native_fn_0205ed58(u32 arg0);
extern u8 native_data_021b8af0[];

u32 native_main_0205f7e0(u32 arg0, u32 arg1, u32 arg2) {
    void *temp_r4;

    if (arg0 < 4U) {
        temp_r4 = native_data_021b8af0 + (arg0 * 8);
        if ((s32) M2C_FIELD(temp_r4, s16 *, 4) >= 0) {
            native_fn_0203a01c(temp_r4,arg1,arg2);
            M2C_FIELD(temp_r4, u8 *, 6) = arg1;
            return native_fn_0205ed58(0U);
        }
        return native_fn_0205ed58(8U);
    }
    return native_fn_0205ed58(0xCU);
}
