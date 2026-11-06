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
typedef struct {
    u32 field_0;
    u32 field_4;
} Record_native_data_020de23c;
extern Record_native_data_020de23c native_data_020de23c;
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    s32 field_4;
} Record_native_data_021c36fc;
extern Record_native_data_021c36fc native_data_021c36fc;
u32 native_main_02067340(u32 arg0) {
    native_data_021c36fc.field_0 = 0;
    native_data_021c36fc.field_4 = 0;
    native_data_020de23c.field_4 = arg0;
    native_data_020de23c.field_0 = arg0;
    return arg0;
}
