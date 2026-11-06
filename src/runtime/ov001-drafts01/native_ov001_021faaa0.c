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
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_0203d294();
extern u32 native_fn_0205c904();
extern u32 native_fn_0205d6f4();
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70();
extern u32 native_fn_ov001_021eec7c();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f1438();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f94d8();
extern u32 native_fn_ov001_021fa164();
extern u32 native_fn_ov001_021fa9d4();
extern u32 native_fn_ov001_02212aac();
extern u8 native_data_ov001_02239a14[];
extern u8 native_data_ov001_02239a5c[];
u32 native_ov001_021faaa0(void) {
    s32 var_r0;

    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0) {
        native_fn_ov001_021f1354(1, 2, 1, 1);
        native_fn_ov001_021f1438(2);
        native_fn_ov001_021fa9d4();
        native_fn_ov001_021eea10(0x10E, 0);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0xAU;
    } else if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0xA) {
        native_fn_0205c904(0x10E);
        native_fn_0202ac08(native_data_ov001_02239a5c);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x15) = (u8) native_fn_ov001_021eec7c(0x10E, M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), 0);
        native_fn_ov001_021f94d8(0x7C, 1);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0x14U;
    }
    if ((M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0x14) && (native_fn_0205d6f4(M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x15)) == 0)) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0x1EU;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0x1E) {
        native_fn_ov001_021f14a4();
        native_fn_ov001_021fa164(0);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x15) = (u8) native_fn_ov001_021eec7c(0x3F, M2C_FIELD(native_data_ov001_02239a14, void **, 0x40), 1);
        if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 6) == 0) {
            if ((s32) native_fn_0207b674(0x4E, M2C_FIELD(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), s32 *, 0x1E8) + 0x46) > 0) {
                M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x20) = (s16) (u8) (native_fn_0203d294(0xBE) + 0xA);
            } else if ((s32) native_fn_0207b674(0x33, M2C_FIELD(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), s32 *, 0x1E8) + 0x46) > 0) {
                M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x20) = (s16) (u8) (native_fn_0203d294(0x5A) + 0xA);
            } else {
                M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x20) = (s16) (u8) (native_fn_0203d294(0x28) + 0xA);
            }
        } else {
            M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x20) = 0;
        }
        M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24) = 0;
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0x28U;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0x28) {
        native_fn_ov001_02212aac(M2C_FIELD(native_data_ov001_02239a14, s8 *, 0x10), M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) + M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24));
        M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24) = (s16) (M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24) + 1);
        if (((s32) (M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) + M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24)) <= 0x3E8) && ((s32) M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24) <= (s32) M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x20))) {

        } else {
            var_r0 = M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) + M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x20);
            if (var_r0 >= 0x3E8) {
                var_r0 = 0x3E8;
            }
            M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16) var_r0;
            native_fn_ov001_02212aac(M2C_FIELD(native_data_ov001_02239a14, s8 *, 0x10), M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26));
            M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x24) = 0;
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0x32U;
        }
    }
    if ((M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0x32) && (native_fn_0205d6f4(M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x15)) == 0)) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0x64U;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) == 0x64) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0x16) = 0U;
        native_fn_0202ac4c(native_data_ov001_02239a5c);
        native_fn_ov001_021eeb70(0x10E);
        M2C_FIELD(native_data_ov001_02239a14, s8 *, 0xA) = 0xA;
    }
    return 0U;
}
