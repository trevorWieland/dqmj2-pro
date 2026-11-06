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
extern u32 native_fn_0207f148();
extern u32 native_fn_0207f49c();
extern u32 native_fn_0207f4dc();
extern u32 native_fn_0207f784();
u32 native_main_02081894(void) {
    native_fn_0207f784(0xF, 8, 6);
    native_fn_0207f49c(0xC);
    return native_fn_0207f148(0, 0x10, 0, 0, native_fn_0207f4dc(), 0, 0);
}
