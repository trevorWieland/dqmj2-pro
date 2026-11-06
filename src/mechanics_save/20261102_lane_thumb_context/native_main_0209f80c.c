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
extern u32 native_fn_02008be0(u32, u32, s32);
extern u32 native_fn_02008c14(u32, u32, s32);
extern u32 native_fn_02008d78(void *, u32, u32);
extern u32 native_fn_0209b368(u32);
extern u32 native_fn_0209be4c(void);
extern u32 native_fn_020a3d70(void);
extern u32 native_fn_020a3d7c(u32 arg0);
u32 native_main_0209f80c(s32 arg0) {
    u32 last_context;
    u32 destination;
    u32 temp_r4;
    u32 temp_r4_2;
    u8 temp_r0;
    u8 var_r0;
    void *temp_r0_2;
    void *temp_r0_3;
    void *temp_r0_4;
    void *temp_r0_5;
    void *temp_r0_6;
    void *temp_r0_7;
    void *temp_r0_8;

    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0xC) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x17C) = 0;
    temp_r4 = native_fn_020a3d70();
    M2C_FIELD(temp_r4, s16 *, 0x17E) = (s16) native_fn_0209b368(0x10000);
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x180) = 0;
    temp_r0_2 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_2, s32 *, 0x184) = 0;
    M2C_FIELD(temp_r0_2, s32 *, 0x188) = 0;
    temp_r0_3 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_3, s32 *, 0x18C) = 0;
    M2C_FIELD(temp_r0_3, s32 *, 0x190) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1A4) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1A9) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1AA) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1AB) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1AC) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1A7) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1A8) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s16 *, 0x1B2) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s16 *, 0x1B4) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x1B8) = 0;
    temp_r0_4 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_4, s32 *, 0x1E0) = 0;
    M2C_FIELD(temp_r0_4, s32 *, 0x1E4) = 0;
    temp_r0_5 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_5, s32 *, 0x1F0) = 0;
    M2C_FIELD(temp_r0_5, s32 *, 0x1F4) = 0;
    native_fn_02008c14(0, native_fn_020a3d70() + 0x3CC, 0x98);
    if (arg0 == 2) {
        temp_r4_2 = native_fn_020a3d70();
        M2C_FIELD(temp_r4_2, u8 *, 0x14) = (u8) M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0xD);
        if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15) == 3) {
            return native_fn_020a3d7c(1U);
        }
        temp_r0 = M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15);
        if (temp_r0 != 2) {
            return (u32) temp_r0;
        }
        return native_fn_020a3d7c(0xAU);
    }
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0xD) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0xE) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x14) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x17) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x20) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0xE8) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1A5) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s16 *, 0x1B0) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x1BC) = 0;
    temp_r0_6 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_6, s32 *, 0x1C0) = 0;
    M2C_FIELD(temp_r0_6, s32 *, 0x1C4) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x1C8) = 0;
    temp_r0_7 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_7, s32 *, 0x1CC) = 0;
    M2C_FIELD(temp_r0_7, s32 *, 0x1D0) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x1D4) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x204) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x208) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x2F0) = 0;
    native_fn_0209be4c();
    destination = native_fn_020a3d70() + 0x24;
    native_fn_02008c14(0, destination, 0x80);
    destination = native_fn_020a3d70() + 0xA4;
    native_fn_02008be0(0, destination, 0x40);
    destination = native_fn_020a3d70() + 0xF4;
    native_fn_02008c14(0, destination, 0x80);
    native_fn_02008c14(0, native_fn_020a3d70() + 0x194, 0xC);
    native_fn_02008c14(0, native_fn_020a3d70() + 0x210, 0x80);
    native_fn_02008be0(0, native_fn_020a3d70() + 0x290, 0x40);
    native_fn_02008d78((void *)(native_fn_020a3d70() + 0x2D0), 0U, 0x20U);
    native_fn_02008c14(0, native_fn_020a3d70() + 0x348, 0x84);
    if (arg0 == 1) {
        if (M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15) == 0) {
            return native_fn_020a3d7c(3U);
        }
        var_r0 = M2C_FIELD((void *) native_fn_020a3d70(), u8 *, 0x15);
        if (var_r0 == 1) {
            return native_fn_020a3d7c(4U);
        }
        
        return (u32) var_r0;
    }
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x15) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x16) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x18) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x20C) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1A6) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1AE) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s8 *, 0x1AD) = 0;
    temp_r0_8 = (void *) native_fn_020a3d70();
    M2C_FIELD(temp_r0_8, s32 *, 0x1F8) = 0;
    M2C_FIELD(temp_r0_8, s32 *, 0x1FC) = 0;
    M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0x46C) = 0;
    last_context = native_fn_020a3d70();
    M2C_FIELD(last_context, s32 *, 0x470) = 0;
    return last_context;
}
