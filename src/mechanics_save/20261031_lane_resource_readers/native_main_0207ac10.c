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
extern int native_fn_0201d444(u8 *, const u8 *, ...);
extern void native_fn_0202a498(s32, void *);
extern u32 native_fn_0202a8e0(const u8 *);
extern u32 native_fn_0203cc2c(u32, u32);
extern u8 native_data_020de4bc[];
extern u8 native_data_021c672c[];

u32 native_main_0207ac10(s32 arg0) {
    u8 sp0[32];
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;

    native_fn_0201d444(sp0, native_data_020de4bc);
    temp_r0_2 = native_fn_0202a8e0(sp0);
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    temp_r0_3 = native_fn_0203cc2c((u32)sp0, (u32)arg0);
    M2C_FIELD(native_data_021c672c, u32 *, 8) = temp_r0_3;
    if (M2C_FIELD(temp_r0_3, s32 *, 0) == 0x50534553) {
        temp_r0 = M2C_FIELD(temp_r0_3, u32 *, 4);
        M2C_FIELD(native_data_021c672c, u32 *, 4) = temp_r0;
        return temp_r0;
    }
    native_fn_0202a498(arg0, (void *) temp_r0_3);
    M2C_FIELD(native_data_021c672c, u32 *, 8) = 0U;
    return (u32) native_data_021c672c;
}
