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
extern u32 ov000_display_context_02215698();
extern u32 native_fn_ov000_022156c4();
extern u32 native_fn_ov000_022156d4();
extern u32 native_fn_ov000_0221570c();
extern u32 native_fn_ov000_022220ac();
u32 native_ov000_0222217c(void) {
    u32 temp_r4;

    temp_r4 = native_fn_ov000_022156c4();
    ov000_display_context_02215698();
    if (native_fn_ov000_022220ac() != 0) {
        native_fn_ov000_022156d4();
        native_fn_ov000_0221570c(1);
    }
    return temp_r4;
}
