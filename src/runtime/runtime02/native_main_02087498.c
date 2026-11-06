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
extern u32 native_fn_02086ce8();
extern u8 native_data_021c9698[];
u32 native_main_02087498(void *arg0, s32 arg1) {
    return native_fn_02086ce8(arg0, (u16) (arg1 + 0xFF95), native_data_021c9698, 8, (s32) (u8) ((M2C_FIELD(arg0, s32 *, 0x24) * M2C_FIELD(arg0, s16 *, 0x76)) + 8), 1);
}
