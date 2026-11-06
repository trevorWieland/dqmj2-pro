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
extern u32 native_fn_020088f8(u32 channel, s32 *data, u32 bytes, void (*callback)(void *), void *context);
extern u32 native_fn_02008afc(u32 channel, s32 *data, u32 bytes, void (*callback)(void *), void *context);
extern void native_fn_0202e300(void);
extern void native_fn_0202e374(void *context);
extern u32 native_fn_0202e434(u32 first, s32 *remaining, u32 words);
extern u8 native_data_020dcb44[];
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    s32 field_8;
} Record_native_data_020edf84;
extern Record_native_data_020edf84 native_data_020edf84;
extern u8 native_data_020edf88[];
u32 native_main_0202e380(s32 *arg0, u32 arg1) {
    if ((arg1 < 0x100U) || (*(u32 *)native_data_020dcb44 == -1)) {
        return native_fn_0202e434(*arg0, arg0 + 1, (arg1 >> 2) - 1);
    }
    native_fn_0202e300();
    native_data_020edf84.field_4 = 1;
    if (native_data_020edf84.field_8 != 0) {
        return native_fn_02008afc(*(u32 *)native_data_020dcb44, arg0, arg1, native_fn_0202e374, native_data_020edf88);
    }
    return native_fn_020088f8(*(u32 *)native_data_020dcb44, arg0, arg1, native_fn_0202e374, native_data_020edf88);
}
