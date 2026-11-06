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
extern u32 native_fn_01ff81e8(void);
extern u32 native_fn_01ff82c8(void);
extern volatile u16 native_data_020e3724;
u32 native_itcm_01ff81b4(void) {
    do {

    } while (native_data_020e3724 == 0);
    *(s16 *)0x04000208 = 0;
    native_fn_01ff82c8();
    return native_fn_01ff81e8();
}
