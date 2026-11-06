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
extern u32 native_fn_02008d78(void *, u32, u32);
extern u32 native_fn_0209f80c(s32);
extern u32 native_fn_020a2ac8(void);
extern u32 native_fn_020a3d64(u32 arg0);
extern u32 native_fn_020a3d70(void);
extern u32 native_fn_020a3d7c(u32 arg0);
extern u8 native_data_021d1b88[];

u32 native_main_0209de84(u8 *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, s32 arg5, s32 arg6, s32 arg7) {
    void *temp_r0;

    native_fn_020a3d64((u32)arg0);
    *(s32 *) native_fn_020a3d70() = arg1;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 4) = arg2;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 8) = arg3;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x10) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x1C) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s16 *, 0x1A) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0xE4) = 0;
    native_fn_020a3d7c(0U);
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0xF) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x19) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1AF) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s16 *, 0x1B6) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x1DC) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x200) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x2F4) = arg4;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x2F8) = arg5;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x2FC) = arg6;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x300) = arg7;
    native_fn_02008d78((void *)(native_fn_020a3d70() + 0x304), 0U, 0x40U);
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x344) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x464) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x468) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x474) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x478) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x47C) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x480) = 0;
    temp_r0 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0, s32 *, 0x174) = 0;
    M2C_FIELD(temp_r0, s32 *, 0x178) = 0;
    native_fn_020a2ac8();
    M2C_FIELD(native_data_021d1b88, s8 *, 0x1C) = 0;
    M2C_FIELD(native_data_021d1b88, s8 *, 0x1D) = 0;
    M2C_FIELD(native_data_021d1b88, s16 *, 0x1E) = 0;
    return native_fn_0209f80c(0);
}
