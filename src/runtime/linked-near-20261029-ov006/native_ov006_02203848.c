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
extern u32 native_fn_02036538();
extern u32 native_fn_ov006_02202dc0();
extern u32 native_fn_ov006_02202dcc();
extern u32 native_fn_ov006_02202e50();
extern u32 native_fn_ov006_02202f54();
u32 native_ov006_02203848(void *arg0, u32 arg1, s32 arg2, u32 arg3, s32 arg4) {
    u32 temp_r0;
    u32 sp10;

    temp_r0 = native_fn_ov006_02202dc0(arg3, 0);
    sp10 = temp_r0;
    native_fn_ov006_02202dcc(arg3, -1, 0, 0);
    native_fn_ov006_02202e50(arg3, -1, 0, 0xF);
    native_fn_ov006_02202f54(arg3, -1, arg4);
    return native_fn_02036538(temp_r0, M2C_FIELD(arg0, u8 *, 0x2E), M2C_FIELD(arg0, u8 *, 0x2F), arg1, arg2, 0, (s32) M2C_FIELD(arg0, u16 *, 0x2C), 2);
}
