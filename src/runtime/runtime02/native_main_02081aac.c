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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0207f4ac();
extern u8 native_data_021c6e50[];
u32 native_main_02081aac(void) {
    if (*native_data_021c6e50 == native_fn_0207f4ac()) {
        native_fn_0205e7a8(-1, 0x52);
        return 1U;
    }
    native_fn_0205e7a8(-1, 0x54);
    return 0U;
}
