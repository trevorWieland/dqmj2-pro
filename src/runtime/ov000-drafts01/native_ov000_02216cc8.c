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
extern u32 native_fn_0204b380();
extern u32 native_fn_ov000_0221767c();
extern u32 native_fn_ov000_02217c9c();
typedef struct {
    u8 unknown_0[0x10];
    s8 field_10;
} Record_native_data_ov000_0224536c;
extern Record_native_data_ov000_0224536c native_data_ov000_0224536c;
extern u8 native_data_ov000_022459b4[];
extern u8 native_data_ov000_022459c4[];
u32 native_ov000_02216cc8(void) {
    native_fn_ov000_02217c9c(1);
    if (native_data_ov000_0224536c.field_10 == 0) {
        native_fn_ov000_0221767c();
        native_fn_0204b380(native_data_ov000_022459c4, 1);
    }
    M2C_FIELD(native_data_ov000_022459b4, s8 *, 0x494) = 4;
    return (u32) native_data_ov000_022459b4;
}
