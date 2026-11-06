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
extern u8 native_data_020dd824[] __attribute__((aligned(2)));
extern u8 native_data_020dd840[];
u32 native_main_0203bd10(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    M2C_FIELD(native_data_020dd824, s32 *, 8) = (s32) ((arg0 * 0x18) + (s32) native_data_020dd840);
    M2C_FIELD(native_data_020dd824, s32 *, 0xC) = (s32) ((arg1 * 0x18) + (s32) native_data_020dd840);
    M2C_FIELD(native_data_020dd824, s32 *, 0x10) = (s32) ((arg2 * 0x18) + (s32) native_data_020dd840);
    M2C_FIELD(native_data_020dd824, s32 *, 0x14) = (s32) ((arg3 * 0x18) + (s32) native_data_020dd840);
    M2C_FIELD(native_data_020dd824, s32 *, 0x18) = (s32) ((arg4 * 0x18) + (s32) native_data_020dd840);
    return (u32) native_data_020dd824;
}
