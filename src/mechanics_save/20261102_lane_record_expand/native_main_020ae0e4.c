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
extern u32 native_fn_020b2a38(void *, const void *, u32);
void native_main_020ae0e4(void *arg0, void *arg1) {
    void *temp_r1;
    void *temp_r1_2;
    void *temp_r1_3;
    void *temp_r1_4;
    void *temp_r1_5;
    void *temp_r1_6;
    void *temp_r1_7;
    void *temp_r1_8;

    temp_r1 = M2C_FIELD(arg0, void **, 0);
    if (temp_r1 != NULL) {
        native_fn_020b2a38(arg1 + 8, temp_r1, 0x1F);
    } else {
        M2C_FIELD(arg1, s8 *, 8) = 0;
    }
    temp_r1_2 = M2C_FIELD(arg0, void **, 4);
    if (temp_r1_2 != NULL) {
        native_fn_020b2a38(arg1 + 0x27, temp_r1_2, 0x15);
    } else {
        M2C_FIELD(arg1, s8 *, 0x27) = 0;
    }
    temp_r1_3 = M2C_FIELD(arg0, void **, 8);
    if (temp_r1_3 != NULL) {
        native_fn_020b2a38(arg1 + 0x3C, temp_r1_3, 0x33);
    } else {
        M2C_FIELD(arg1, s8 *, 0x3C) = 0;
    }
    temp_r1_4 = M2C_FIELD(arg0, void **, 0xC);
    if (temp_r1_4 != NULL) {
        native_fn_020b2a38(arg1 + 0x6F, temp_r1_4, 0x1F);
    } else {
        M2C_FIELD(arg1, s8 *, 0x6F) = 0;
    }
    temp_r1_5 = M2C_FIELD(arg0, void **, 0x10);
    if (temp_r1_5 != NULL) {
        native_fn_020b2a38(arg1 + 0x8E, temp_r1_5, 0x1F);
    } else {
        M2C_FIELD(arg1, s8 *, 0x8E) = 0;
    }
    temp_r1_6 = M2C_FIELD(arg0, void **, 0x14);
    if (temp_r1_6 != NULL) {
        native_fn_020b2a38(arg1 + 0xAD, temp_r1_6, 0x4C);
    } else {
        M2C_FIELD(arg1, s8 *, 0xAD) = 0;
    }
    M2C_FIELD(arg1, s32 *, 0xFC) = (s32) M2C_FIELD(arg0, s32 *, 0x18);
    native_fn_020b2a38(arg1 + 0x100, arg0 + 0x1C, 0xB);
    native_fn_020b2a38(arg1 + 0x10B, arg0 + 0x27, 3);
    M2C_FIELD(arg1, s32 *, 0x110) = (s32) M2C_FIELD(arg0, s32 *, 0x2C);
    M2C_FIELD(arg1, s32 *, 0x114) = (s32) M2C_FIELD(arg0, s32 *, 0x30);
    temp_r1_7 = arg0 + 0x34;
    if (temp_r1_7 != NULL) {
        native_fn_020b2a38(arg1 + 0x118, temp_r1_7, 0x80);
    } else {
        M2C_FIELD(arg1, s8 *, 0x118) = 0;
    }
    M2C_FIELD(arg1, s32 *, 0x198) = (s32) M2C_FIELD(arg0, s32 *, 0xB4);
    M2C_FIELD(arg1, s32 *, 0x19C) = (s32) M2C_FIELD(arg0, s32 *, 0xB8);
    M2C_FIELD(arg1, s32 *, 0x1A0) = (s32) M2C_FIELD(arg0, s32 *, 0xBC);
    M2C_FIELD(arg1, s32 *, 0x1A4) = (s32) M2C_FIELD(arg0, s32 *, 0xC0);
    M2C_FIELD(arg1, s32 *, 0x1A8) = (s32) M2C_FIELD(arg0, s32 *, 0xC4);
    temp_r1_8 = M2C_FIELD(arg0, void **, 0xC8);
    if (temp_r1_8 != NULL) {
        native_fn_020b2a38(arg1 + 0x1AC, temp_r1_8, 0x33);
    } else {
        M2C_FIELD(arg1, s8 *, 0x1AC) = 0;
    }
    M2C_FIELD(arg1, s32 *, 0xFC) = (s32) M2C_FIELD(arg0, s32 *, 0x18);
    M2C_FIELD(arg1, s32 *, 0x110) = (s32) M2C_FIELD(arg0, s32 *, 0x2C);
    M2C_FIELD(arg1, s32 *, 0x114) = (s32) M2C_FIELD(arg0, s32 *, 0x30);
    M2C_FIELD(arg1, s32 *, 0x198) = (s32) M2C_FIELD(arg0, s32 *, 0xB4);
    M2C_FIELD(arg1, s32 *, 0x19C) = (s32) M2C_FIELD(arg0, s32 *, 0xB8);
    M2C_FIELD(arg1, s32 *, 0x1A0) = (s32) M2C_FIELD(arg0, s32 *, 0xBC);
    M2C_FIELD(arg1, s32 *, 0x1A4) = (s32) M2C_FIELD(arg0, s32 *, 0xC0);
    M2C_FIELD(arg1, s32 *, 0x1A8) = (s32) M2C_FIELD(arg0, s32 *, 0xC4);
    M2C_FIELD(arg1, s32 *, 0x1E0) = (s32) M2C_FIELD(arg0, s32 *, 0xCC);
    M2C_FIELD(arg1, s32 *, 0x1E4) = (s32) M2C_FIELD(arg0, s32 *, 0xD0);
    M2C_FIELD(arg1, s32 *, 0x1E8) = (s32) M2C_FIELD(arg0, s32 *, 0xD4);
    M2C_FIELD(arg1, s32 *, 0x1EC) = (s32) M2C_FIELD(arg0, s32 *, 0xD8);
    M2C_FIELD(arg1, s32 *, 0x1F0) = (s32) M2C_FIELD(arg0, s32 *, 0xDC);
    M2C_FIELD(arg1, s32 *, 0x1F4) = (s32) M2C_FIELD(arg0, s32 *, 0xE0);
    M2C_FIELD(arg1, s32 *, 0x1F8) = (s32) M2C_FIELD(arg0, s32 *, 0xE4);
    M2C_FIELD(arg1, s32 *, 0x1FC) = (s32) M2C_FIELD(arg0, s32 *, 0xE8);
    M2C_FIELD(arg1, s32 *, 0x200) = (s32) M2C_FIELD(arg0, s32 *, 0xEC);
}
