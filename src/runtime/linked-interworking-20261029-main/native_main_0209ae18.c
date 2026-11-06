#define NULL ((void *)0)
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
extern u32 native_fn_02006b7c();
extern u32 native_fn_020944c0();
extern u32 native_fn_02096948();
extern u32 native_fn_02096b68();
extern u32 native_fn_02096b7c();
extern u8 native_data_021d19bc[];
u32 native_main_0209ae18(void) {
    if (M2C_FIELD(native_data_021d19bc, void **, 4) != NULL) {
        if (M2C_FIELD(M2C_FIELD(native_data_021d19bc, void **, 4), u16 *, 4) == 1) {
            if (M2C_FIELD(M2C_FIELD(native_data_021d19bc, void **, 4), s32 *, 0x10) == 1) {
                native_fn_02096b68();
                do {

                } while ((u32) (native_fn_02096948() - 2) > 2U);
                native_fn_02096b7c();
            }
            M2C_FIELD(native_data_021d19bc, void **, 4) = NULL;
            return (u32) native_data_021d19bc;
        }
        if (native_fn_020944c0() == 0) {
            do {
                native_fn_02006b7c(0xA);
            } while (native_fn_020944c0() == 0);
        }
        M2C_FIELD(native_data_021d19bc, void **, 4) = NULL;
        
        return (u32) native_data_021d19bc;
    }
    return (u32) native_data_021d19bc;
}
