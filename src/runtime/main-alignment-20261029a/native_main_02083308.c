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
extern u32 native_fn_02013ffc();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_02083360();
typedef struct {
    u8 unknown_0[0x34];
    s32 field_34;
} Record_native_data_021c72a0;
extern Record_native_data_021c72a0 native_data_021c72a0 __attribute__((aligned(2)));
extern u8 native_data_021c76c0[];
u32 native_main_02083308(void) {
    if (native_data_021c72a0.field_34 != 6) {
        return 0U;
    }
    native_fn_020824b4(3);
    if (native_fn_02013ffc(native_data_021c76c0) != 0) {
        native_fn_020824c4();
        return 0U;
    }
    if (native_fn_02083360() == 0) {
        return 0U;
    }
    return 1U;
}
