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
extern void native_fn_02061c1c();
extern void native_fn_0206e2fc();
extern void native_fn_0206e388();
extern void native_fn_0206e634();
extern void native_fn_0206e6c0();
extern u8 native_data_ov000_02238190[];
u32 native_ov000_02204dec(void) {
    if (M2C_FIELD(native_data_ov000_02238190, u8 *, 6) != 0) {
        return (u32) M2C_FIELD(native_data_ov000_02238190, u8 *, 6);
    }
    native_fn_02061c1c(3, 8, 2, 0x10, 2, 0, 1);
    native_fn_02061c1c(0, 2, 0x11, 0x16, 2, 0, 1);
    native_fn_02061c1c(1, 3, 0x13, 0x18, 2, 0, 1);
    native_fn_02061c1c(2, 3, 0x15, 0x18, 2, 0, 1);
    native_fn_0206e2fc(0, 0, 0xD, 0, 0);
    native_fn_0206e2fc(1, 0x1F, 0xD, 1, 0);
    native_fn_0206e634(2);
    native_fn_0206e6c0(M2C_FIELD(native_data_ov000_02238190, u8 *, 7));
    native_fn_0206e388(4, 5);
    M2C_FIELD(native_data_ov000_02238190, u8 *, 6) = 1U;
    return (u32) native_data_ov000_02238190;
}
