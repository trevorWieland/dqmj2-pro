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
extern u32 native_fn_02038148(void *,u32,u32);
extern u32 native_fn_0205ed58(s8);
extern u8 native_data_021b8b10[];
u32 native_main_0205f6a0(u32 arg0, u32 arg1, u32 arg2) {
    void *temp_r4;

    if (arg0 < 0x10U) {
        temp_r4 = native_data_021b8b10 + (arg0 * 8);
        if ((s32) M2C_FIELD(temp_r4, s16 *, 4) >= 0) {
            if (arg1 <= 0x7FU) {
                native_fn_02038148(temp_r4,arg1,arg2);
                M2C_FIELD(temp_r4, s8 *, 6) = (s8) arg1;
                return native_fn_0205ed58(0);
            }
            return native_fn_0205ed58(0x10);
        }
        return native_fn_0205ed58(8);
    }
    return native_fn_0205ed58(0xC);
}
