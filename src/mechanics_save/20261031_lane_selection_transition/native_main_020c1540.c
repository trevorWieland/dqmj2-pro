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
extern u32 native_fn_0205e7a8(s32, s32);
extern u32 native_fn_02069000(void);
extern u32 native_fn_0206c1d4(u32, u8 *, u8 *);
extern u32 native_fn_020bf6c4(void);
extern u32 native_fn_020c01f0(void);
extern u32 native_fn_020c0200(void);
extern u32 native_fn_020c0210(void);
extern u32 native_fn_020c1794(void);
extern u32 native_fn_020c1a04(s32, s32, s32 *, s32);
extern u8 native_data_021d4bec[];

u32 native_main_020c1540(void) {
    s32 sp4;
    u8 sp1;
    u8 sp0;
    u32 temp_r4;

    native_fn_0206c1d4(native_fn_02069000(), &sp1, &sp0);
    sp4 = (s32) M2C_FIELD(native_data_021d4bec, u8 *, 4);
    M2C_FIELD(native_data_021d4bec, u8 *, 0) = (u8) M2C_FIELD(native_data_021d4bec, u8 *, 4);
    temp_r4 = native_fn_020c1a04((sp1 + 0xB) * 8, (sp0 + 1) * 8, &sp4, native_fn_020bf6c4());
    M2C_FIELD(native_data_021d4bec, u8 *, 4) = (u8) sp4;
    if ((M2C_FIELD(native_data_021d4bec, u8 *, 4) != M2C_FIELD(native_data_021d4bec, u8 *, 0)) && (temp_r4 != 0)) {
        native_fn_020c0210();
        if (native_fn_020c1794() == 0) {
            native_fn_020c01f0();
        } else {
            native_fn_020c0200();
        }
        native_fn_0205e7a8(-1, 0x56);
    }
    M2C_FIELD(native_data_021d4bec, u8 *, 0) = (u8) M2C_FIELD(native_data_021d4bec, u8 *, 4);
    return temp_r4;
}
