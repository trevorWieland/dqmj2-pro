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
#define NULL ((void *)0)
extern void native_fn_02008d78(void *destination,int value,u32 bytes);
extern void native_fn_02008e0c(const void *source,void *destination,u32 bytes);
extern const u8 *native_fn_02062a10(u32 id);
extern u32 native_fn_020c384c(u32 count);
extern u8 native_data_021d4cf4[];
extern u8 native_data_021d4d48[];
extern u8 native_data_021d4d68[];
u32 native_main_020c3790(const u32 *arg0) {
    const u8 *temp_r0;
    u8 var_r7;
    u8 var_r8;

    var_r8 = 0;
    native_fn_02008d78(native_data_021d4d68, 0, 0x18C);
    native_fn_02008d78(native_data_021d4d48, 0, 0xC);
    var_r7 = 0;
    do {
        temp_r0 = native_fn_02062a10(arg0[var_r7]);
        if (temp_r0 != 0) {
            M2C_FIELD((native_data_021d4cf4 + (var_r8 * 4)), s32 *, 0x54) = (s32) arg0[var_r7];
            native_fn_02008e0c(temp_r0, (var_r8 * 0x84) + (s32) native_data_021d4d68, 0x84);
            var_r8 += 1;
        }
        var_r7 += 1;
    } while ((u32) var_r7 < 3U);
    return native_fn_020c384c(var_r8);
}
