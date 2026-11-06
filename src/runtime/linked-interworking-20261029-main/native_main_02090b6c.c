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
extern u32 native_fn_02006acc();
extern u32 native_fn_02006b74();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_020de830;
extern Record_native_data_020de830 native_data_020de830;
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_020e33e4;
extern Record_native_data_020e33e4 native_data_020e33e4;
u32 native_main_02090b6c(void) {
    u32 temp_r4;
    s32 temp_r5;

    if ((u32) native_data_020de830.field_4 < 0x20U) {
        temp_r5 = native_data_020e33e4.field_4;
        temp_r4 = native_fn_02006b74(temp_r5);
        native_fn_02006acc(temp_r5, native_data_020de830.field_4);
        return temp_r4;
    }
    return -1U;
}
