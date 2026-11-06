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
u32 native_main_0202fb98(void *arg0) {
    s32 temp_r0_2;
    s32 var_r0;
    s32 var_r0_2;
    void *temp_r0;
    s32 temp_r1;
    u8 temp_r4;
    u8 var_r5;
    void *temp_ip;

    if (!(M2C_FIELD(arg0, s32 *, 8) & 0x200)) {
        temp_r4 = M2C_FIELD(M2C_FIELD(arg0, void **, 0), u8 *, 1);
        M2C_FIELD(arg0, u8 *, 0xAC) = temp_r4;
        M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) | 4);
        M2C_FIELD(arg0, s32 **, 0xB8) = (s32 *) (arg0 + 0x184);
        if (M2C_FIELD(arg0, u32 (**)(void *), 0x14) != NULL) {
            var_r5 = M2C_FIELD(arg0, u8 *, 0x8E);
        } else {
            var_r5 = 0;
        }
        if (var_r5 == 1) {
            M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) & ~0x40);
            M2C_FIELD(arg0, u32 (**)(void *), 0x14)(arg0);
            if (M2C_FIELD(arg0, u32 (**)(void *), 0x14) != NULL) {
                var_r5 = M2C_FIELD(arg0, u8 *, 0x8E);
            } else {
                var_r5 = 0;
            }
            var_r0 = M2C_FIELD(arg0, s32 *, 8) & 0x40;
        } else {
            var_r0 = 0;
        }
        if ((var_r0 == 0) && ((temp_ip = M2C_FIELD(arg0, void **, 4), temp_r1 = M2C_FIELD(temp_ip, s32 *, 0x18), (temp_r1 == 0)) || !(M2C_FIELD((temp_ip + (((u32) temp_r4 >> 5) * 4)), s32 *, 0x4C) & (1U << (temp_r4 & 0x1F))) || (M2C_FIELD(temp_ip, s32 (**)(s32 *, s32, u8), 0x1C)(M2C_FIELD(arg0, s32 **, 0xB8), temp_r1, temp_r4) == 0))) {
            *M2C_FIELD(arg0, s32 **, 0xB8) = M2C_FIELD(M2C_FIELD(arg0, void **, 0), u8 *, 2) & 1;
        }
        if (var_r5 == 2) {
            M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) & ~0x40);
            M2C_FIELD(arg0, u32 (**)(void *), 0x14)(arg0);
            if (M2C_FIELD(arg0, u32 (**)(void *), 0x14) != NULL) {
                var_r5 = M2C_FIELD(arg0, u8 *, 0x8E);
            } else {
                var_r5 = 0;
            }
            var_r0_2 = M2C_FIELD(arg0, s32 *, 8) & 0x40;
        } else {
            var_r0_2 = 0;
        }
        if (var_r0_2 == 0) {
            temp_r0_2 = *M2C_FIELD(arg0, s32 **, 0xB8);
            if (temp_r0_2 != 0) {
                M2C_FIELD(arg0, s32 *, 8) |= 1;
            } else {
                M2C_FIELD(arg0, s32 *, 8) &= ~1;
            }
        }
        if (var_r5 == 3) {
            M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) & ~0x40);
            M2C_FIELD(arg0, u32 (**)(void *), 0x14)(arg0);
        }
    }
    temp_r0 = M2C_FIELD(arg0, void **, 0) + 3;
    M2C_FIELD(arg0, void **, 0) = temp_r0;
    return (u32) temp_r0;
}
