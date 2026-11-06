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
extern u32 native_fn_0207e874();
extern u32 native_fn_0207f390();
extern u32 native_fn_02081c9c();
extern u32 native_fn_ov006_021e648c();
extern u32 native_fn_ov006_021e7a00();
extern u32 native_fn_ov006_02204dfc();
u32 native_ov006_02204c40(s32 arg0) {
    if ((arg0 != 0) && (native_fn_0207e874() != 0)) {
        native_fn_ov006_021e7a00(0);
        if ((native_fn_0207f390() != 0) && (native_fn_02081c9c() == 0xC)) {
            native_fn_ov006_02204dfc();
            return -2U;
        }
        return -1U;
    }
    return native_fn_ov006_021e648c(arg0);
}
