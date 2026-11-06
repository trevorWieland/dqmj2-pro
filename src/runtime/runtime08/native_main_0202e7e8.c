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
extern u32 native_fn_0202e790();
extern u8 native_data_020edf90[];
extern u8 native_data_020ee0c0[];
u32 native_main_0202e7e8(void) {
    if (!(M2C_FIELD(native_data_020edf90, s32 *, 0xFC) & 0x80)) {
        native_fn_0202e790();
        M2C_FIELD(native_data_020edf90, s32 *, 0xFC) = (s32) (M2C_FIELD(native_data_020edf90, s32 *, 0xFC) | 0x80);
    }
    return (u32) native_data_020ee0c0;
}
