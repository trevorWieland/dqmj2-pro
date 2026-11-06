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
extern u32 native_fn_0205bf4c();
extern u32 native_fn_ov000_021d900c();
extern u32 native_fn_ov000_021d9088();
extern u32 native_fn_ov000_021d92b4();
extern u32 native_fn_ov000_021d9580();
extern u32 native_fn_ov000_021d966c();
extern u32 native_fn_ov000_021d99ac();
extern u32 native_fn_ov000_021da08c();
extern u32 native_fn_ov000_021da454();
extern u32 native_fn_ov000_02211530();
extern u32 native_fn_ov000_02211830();
u32 native_ov000_021e767c(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_ov000_021d900c() != 0) {
        native_fn_ov000_021d92b4(0xFF);
        native_fn_ov000_021d9580(0xFF);
        native_fn_ov000_021d9088();
        native_fn_ov000_021da454(0xFF);
        native_fn_ov000_021d966c(0xFF);
        native_fn_ov000_021d99ac(0);
        native_fn_0205bf4c();
        native_fn_ov000_021da08c();
        native_fn_ov000_02211530();
        native_fn_ov000_02211830();
        var_r4 = 1;
    }
    return var_r4;
}
