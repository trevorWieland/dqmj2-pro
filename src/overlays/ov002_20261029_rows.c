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
extern void native_fn_ov002_021d7998(s32, s32, s32, s32, s32, s32, s32, s32, s32);
extern void native_fn_ov002_021d7a50(void *, s32, u32, s32, s32, s32, s32, s32);
void native_ov002_021d7f98(void *arg0, s32 arg1, u32 arg2, u8 arg3, u8 arg4, s32 arg5, s32 arg6) {
    u8 var_r5;
    s32 sp14;

    sp14 = arg1;
    native_fn_ov002_021d7998(4, M2C_FIELD(arg0, s8 *, 0x10), 0xC, (u8) (arg3 - 1), (s32) (u8) (arg4 - 1), (s32) (u8) ((u32) arg5 + 2U), (s32) (u8) ((arg2 * 2) + 2), 1, 0);
    var_r5 = 0;
    if ((u32) var_r5 < arg2) {
        do {
            native_fn_ov002_021d7998((s8) (var_r5 + 5), M2C_FIELD(arg0, s8 *, 0x10), 1, arg3, (s32) (u8) (arg4 + (var_r5 * 2)), arg5, 2, 0, 1);
            var_r5 += 1;
        } while ((u32) var_r5 < arg2);
    }
    native_fn_ov002_021d7a50(arg0, sp14, arg2, 5, 0, 1, 0, arg6);
}
