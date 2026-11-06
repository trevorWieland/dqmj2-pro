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
extern u32 native_fn_0205dbf0();
extern u32 native_fn_0205df8c();
extern u8 native_data_020dc348[];
extern u8 native_data_020dc368[];
extern u8 native_data_021cebe0[];
extern u8 native_data_021cec18[];
u32 native_main_02089590(void) {
    if (M2C_FIELD(native_data_021cebe0, s32 *, 0x38) != 0) {
        native_fn_0205dbf0(1, native_data_021cec18, native_data_020dc368, native_data_020dc348, 0x10);
        native_fn_0205df8c(0);
    }
    M2C_FIELD(native_data_021cebe0, s32 *, 0x38) = 0;
    return (u32) native_data_021cebe0;
}
