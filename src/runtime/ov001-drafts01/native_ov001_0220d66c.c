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
extern u32 native_fn_02065e44();
u32 native_ov001_0220d66c(void *arg0, s32 arg1) {
    void *temp_ip;

    temp_ip = M2C_FIELD(arg0, void **, 0x1E8);
    return native_fn_02065e44(arg0 + 0x1EC, temp_ip + 0xDC, M2C_FIELD(temp_ip, s16 *, 0x2A), M2C_FIELD(temp_ip, u8 *, 0x2C), temp_ip + 0x46, arg1, arg0);
}
