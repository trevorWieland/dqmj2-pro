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
extern u32 native_fn_ov001_021e865c();
extern u32 native_fn_ov001_0220946c();
u32 native_ov001_021dc940(void *arg0, s32 arg1) {
    u32 temp_r4;

    temp_r4 = native_fn_ov001_0220946c(arg0 + 0x22C);
    if ((arg1 != 0xB) && (arg1 != 0xA) && (arg1 != 9) && (arg1 != 0xC) && (arg1 != 0xD) && (arg1 != 0xE) && (arg1 != 0xF) && (arg1 != 0x22) && (arg1 != 0x20)) {

    } else if (temp_r4 != 0) {
        native_fn_ov001_021e865c(M2C_FIELD(arg0, u8 *, 0x31E), M2C_FIELD(arg0, u8 *, 0x31F));
    }
    return temp_r4;
}
