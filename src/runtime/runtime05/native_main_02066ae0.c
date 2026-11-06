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
extern u32 native_fn_0200ddf4();
extern u32 native_fn_0200de88();
extern u32 native_fn_0200e26c();
extern u8 native_data_021c36d8[];
extern u8 native_data_021c36e0[];
u32 native_main_02066ae0(void) {
    s32 var_r0;

    var_r0 = (s32) (*(u16 *)0x027FFFA8 & 0x8000) >> 0xF;
    if (var_r0 == 0) {
        do {
            native_fn_0200ddf4((u32) var_r0);
            var_r0 = (s32) native_fn_0200de88(native_data_021c36e0);
        } while (var_r0 != 0);
        native_fn_0200e26c(native_data_021c36d8, native_data_021c36e0);
    }
    return (u32) native_data_021c36d8;
}
