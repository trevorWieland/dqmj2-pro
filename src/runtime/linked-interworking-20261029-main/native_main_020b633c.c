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
extern u32 native_fn_0201af84();
u32 native_main_020b633c(void *arg0) {
    s32 temp_r0;
    u16 temp_r0_2;
    u16 temp_r1;
    u16 temp_r1_2;
    u16 temp_r2;
    s32 temp_r4;
    s32 temp_r6;

    M2C_FIELD(arg0, s32 *, 0x8C) = 6;
    M2C_FIELD(arg0, s32 *, 0x88) = 4;
    M2C_FIELD(arg0, s32 *, 0xD4) = 1;
    temp_r0 = M2C_FIELD(arg0, s32 *, 0x9C);
    if ((temp_r0 == 0) || (M2C_FIELD(arg0, s32 *, 0xAC) == 0) || (M2C_FIELD(arg0, s32 *, 0xBC) == 0)) {
        return 0U;
    }
    temp_r4 = M2C_FIELD(arg0, s32 *, 0x84);
    if ((temp_r4 == 0) && (M2C_FIELD(arg0, s32 *, 0x80) == 0) && (temp_r0 == M2C_FIELD(arg0, s32 *, 0x94))) {
        M2C_FIELD(arg0, s32 *, 0x8C) = 0;
    } else if (temp_r0 == M2C_FIELD(arg0, s32 *, 0x94)) {
        M2C_FIELD(arg0, s32 *, 0x8C) = 1;
    } else {
        temp_r6 = M2C_FIELD(arg0, s32 *, 0x80);
        if ((temp_r6 == 0) && (temp_r4 == 0) && ((s32) native_fn_0201af84(M2C_FIELD(arg0, u16 *, 0xC0) - M2C_FIELD(arg0, u16 *, 0xB0)) >= 1)) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 5;
            M2C_FIELD(arg0, s32 *, 0x88) = 0;
        } else if ((temp_r6 != 0) && (temp_r4 == 0) && ((s32) native_fn_0201af84(M2C_FIELD(arg0, u16 *, 0xC0) - M2C_FIELD(arg0, u16 *, 0xB0)) >= 1)) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 5;
            M2C_FIELD(arg0, s32 *, 0x88) = 2;
        } else if ((temp_r6 == 0) && (temp_r4 != 0) && ((s32) native_fn_0201af84(M2C_FIELD(arg0, u16 *, 0xC0) - M2C_FIELD(arg0, u16 *, 0xB0)) >= 1)) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 5;
            M2C_FIELD(arg0, s32 *, 0x88) = 3;
        } else if ((temp_r6 != 0) && (temp_r4 != 0) && ((s32) native_fn_0201af84(M2C_FIELD(arg0, u16 *, 0xC0) - M2C_FIELD(arg0, u16 *, 0xB0)) >= 1)) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 5;
            M2C_FIELD(arg0, s32 *, 0x88) = 1;
        } else if (temp_r4 != 0) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 4;
        } else if ((temp_r6 != 0) && (temp_r4 == 0)) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 3;
        } else if ((temp_r6 == 0) && (temp_r4 == 0)) {
            M2C_FIELD(arg0, s32 *, 0x8C) = 2;
        } else {
            M2C_FIELD(arg0, s32 *, 0x8C) = 6;
        }
    }
    temp_r2 = M2C_FIELD(arg0, u16 *, 0x98);
    temp_r0_2 = M2C_FIELD(arg0, u16 *, 0xA0);
    if ((temp_r0_2 == temp_r2) && (M2C_FIELD(arg0, u16 *, 0xB0) == M2C_FIELD(arg0, u16 *, 0xA8)) && (M2C_FIELD(arg0, u16 *, 0xC0) == M2C_FIELD(arg0, u16 *, 0xB8))) {
        M2C_FIELD(arg0, s32 *, 0x90) = 1;
    } else {
        temp_r1 = M2C_FIELD(arg0, u16 *, 0xB0);
        if ((temp_r0_2 == temp_r1) && (temp_r1 == M2C_FIELD(arg0, u16 *, 0xC0))) {
            M2C_FIELD(arg0, s32 *, 0x90) = 2;
        } else if ((temp_r0_2 == temp_r2) && ((M2C_FIELD(arg0, u16 *, 0xC0) - temp_r1) == 1)) {
            M2C_FIELD(arg0, s32 *, 0x90) = 4;
        } else if ((M2C_FIELD(arg0, u16 *, 0xC0) - temp_r1) == 1) {
            M2C_FIELD(arg0, s32 *, 0x90) = 3;
        } else {
            M2C_FIELD(arg0, s32 *, 0x90) = 0;
        }
    }
    temp_r1_2 = M2C_FIELD(arg0, u16 *, 0xD0);
    if ((temp_r1_2 != 0) && (M2C_FIELD(arg0, u16 *, 0xA0) != temp_r1_2)) {
        M2C_FIELD(arg0, s32 *, 0xD4) = 0;
    }
    return 1U;
}
