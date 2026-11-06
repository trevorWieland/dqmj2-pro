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
extern u32 native_fn_020040ec(void);
extern void native_fn_02008d78(void *,u32,u32);
extern u32 native_fn_02061944(void);
extern u32 native_fn_02061bf0(void);
extern void native_fn_020cb354(void);
extern u32 native_fn_020cbbf0(void);
extern u8 native_data_021d6620[];
extern u8 native_data_021d6630[];
u32 native_main_020cb090(void) {
    u8 *temp_r4;
    u32 base;

    temp_r4 = (u8 *)native_fn_02061944();
    native_fn_02008d78(native_data_021d6630, 0, 0xE4);
    M2C_FIELD(native_data_021d6630, s32 *, 0xE0) = (s32) M2C_FIELD(temp_r4, s32 *, 0x25C);
    base = native_fn_020040ec();
    base += (u32)M2C_FIELD(native_data_021d6630, s32 *, 0xE0);
    native_fn_02008d78((void *)base, 0, 0x1C20);
    native_fn_02061bf0();
    native_fn_020cb354();
    native_fn_020cbbf0();
    M2C_FIELD(native_data_021d6620, s32 *, 0xC) = 1;
    M2C_FIELD(native_data_021d6620, s8 *, 4) = 1;
    return (u32) native_data_021d6620;
}
