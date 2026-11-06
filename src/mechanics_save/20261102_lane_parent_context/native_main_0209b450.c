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
extern u32 native_fn_02008e0c(const void *, void *, u32);
extern u32 native_fn_0201d69c(s8 *arg0);
extern u32 native_fn_0209a9d0(void);
extern u32 native_fn_0209bd94(void);
extern u32 native_fn_0209bff8(u32 arg0, u32 arg1);
extern u32 native_fn_0209c24c();
extern u32 native_fn_0209c254();
extern u32 native_fn_0209c4c0();
extern u32 native_fn_0209c4f0(u32, u32, u32, s32, s32, u32, u32, u32);
extern u32 native_fn_0209cdac(u32, u32, u32, s32, s32);
extern u32 native_fn_0209de84(u8 *, s32, s32, s32, s32, s32, s32, s32);
extern u32 native_fn_0209ef04();
extern u32 native_fn_020a4188(void *);
extern void * native_data_021d19e0;
extern u8 native_data_021d2544[];
extern u8 native_data_021d2644[];

void native_main_0209b450(void *arg0, void *arg1, s32 arg2, u32 arg3, u32 arg4, s32 arg5, s32 arg6, s32 arg7, s32 arg8) {
    s32 var_r1;
    s32 var_r2;
    u32 var_r4;
    u32 var_r5;

    native_data_021d19e0 = arg0;
    native_fn_0209a9d0();
    M2C_FIELD(native_data_021d19e0, s32 *, 0) = 0;
    M2C_FIELD(native_data_021d19e0, u32 (**)(), 4) = native_fn_0209ef04;
    M2C_FIELD(native_data_021d19e0, u32 (**)(), 8) = native_fn_0209c24c;
    M2C_FIELD(native_data_021d19e0, u32 (**)(), 0xC) = native_fn_0209c254;
    M2C_FIELD(native_data_021d19e0, u32 (**)(), 0x10) = native_fn_0209c4c0;
    var_r1 = arg5;
    if (var_r1 == 0) {
        var_r1 = 0x2000;
    }
    M2C_FIELD(native_data_021d19e0, s32 *, 0x14) = var_r1;
    var_r2 = arg6;
    if (var_r2 == 0) {
        var_r2 = 0x2000;
    }
    M2C_FIELD(native_data_021d19e0, s32 *, 0x18) = var_r2;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x1C) = 0;
    M2C_FIELD(native_data_021d19e0, void **, 0x20) = arg1;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x24) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x28) = 0;
    M2C_FIELD(native_data_021d19e0, s8 *, 0x2C) = 0;
    M2C_FIELD(native_data_021d19e0, s8 *, 0x2D) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x64) = 0;
    M2C_FIELD(native_data_021d19e0, void **, 0x68) = native_data_021d2544;
    M2C_FIELD(native_data_021d19e0, void **, 0x6C) = native_data_021d2644;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x70) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x74) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x78) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x7C) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x80) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x84) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x88) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x8C) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x90) = 0;
    M2C_FIELD(native_data_021d19e0, s32 *, 0x94) = 0;
    native_fn_0209bd94();
    native_fn_0209c4f0((u32)((u8 *)native_data_021d19e0 + 0x98), (u32)arg1, (u32)((u8 *)native_data_021d19e0 + 0x1C), arg2, M2C_FIELD(arg1, s32 *, 0x24), (u32)((u8 *)native_data_021d19e0 + 0x2E), (u32)native_fn_0209bff8, 0);
    native_fn_0209cdac((u32)((u8 *)native_data_021d19e0 + 0x318), (u32)((u8 *)native_data_021d19e0 + 0x1C), (u32)((u8 *)native_data_021d19e0 + 0x2E), arg7, arg8);
    native_fn_0209de84((u8 *)native_data_021d19e0 + 0x378, (s32)(u32)((u8 *)native_data_021d19e0 + 0x1C), (s32)(u32)native_data_021d19e0, (s32)(u32)((u8 *)native_data_021d19e0 + 4), (s32)(u32)native_data_021d2544, (s32)(u32)native_data_021d2644, arg7, arg8);
    native_fn_020a4188((u8 *)native_data_021d19e0 + 0x7FC);
    if (native_fn_0201d69c((s8 *)arg3) < 0x100U) {
        var_r5 = native_fn_0201d69c((s8 *)arg3);
    } else {
        var_r5 = 0xFF;
    }
    native_fn_02008e0c((void *) arg3, native_data_021d2544, var_r5);
    *(native_data_021d2544 + var_r5) = 0;
    if (native_fn_0201d69c((s8 *)arg4) < 0x100U) {
        var_r4 = native_fn_0201d69c((s8 *)arg4);
    } else {
        var_r4 = 0xFF;
    }
    native_fn_02008e0c((void *) arg4, native_data_021d2644, var_r4);
    *(native_data_021d2644 + var_r4) = 0;

}
