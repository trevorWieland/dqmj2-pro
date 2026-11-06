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
extern u32 native_fn_02001114();
extern u32 native_fn_02001148();
extern u32 native_fn_020014d4();
extern u8 native_data_020edf90[];
extern u8 native_data_020edfdc[];
extern u8 native_data_020ee04c[];
extern u8 native_data_020ee0c0[];
extern u8 native_data_020ee0f0[];
u32 native_main_0202e790(void) {
    native_fn_020014d4(native_data_020ee04c, native_data_020edfdc, native_data_020ee0c0);
    native_fn_02001114(native_data_020ee0c0, native_data_020ee0c0, M2C_FIELD(native_data_020edf90, s32 *, 0xEC), M2C_FIELD(native_data_020edf90, s32 *, 0xF0), M2C_FIELD(native_data_020edf90, s32 *, 0xF4));
    return native_fn_02001148(native_data_020ee0c0, native_data_020ee0f0);
}
