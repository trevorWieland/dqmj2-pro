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
extern u32 native_fn_02048a6c();
extern u32 native_fn_0205f98c();
u32 native_ov001_02211cec(void *arg0) {
    s16 temp_r1;
    s32 temp_r1_3;
    s8 temp_r1_2;
    u8 var_r7;
    void *temp_r0;

    var_r7 = 1;
    M2C_FIELD(arg0, s16 *, 0x26) = (s16) (M2C_FIELD(arg0, s16 *, 0x26) - 2);
    if ((u32) M2C_FIELD(arg0, u8 *, 0x22) > 1U) {
        do {
            temp_r0 = (void *) native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), var_r7);
            temp_r1 = M2C_FIELD(temp_r0, s16 *, 0x82);
            if ((s32) temp_r1 > 0) {
                M2C_FIELD(temp_r0, s16 *, 0x82) = (s16) (temp_r1 - 2);
            } else {
                temp_r1_2 = M2C_FIELD(temp_r0, s8 *, 0x88);
                if ((s32) temp_r1_2 > 0) {
                    M2C_FIELD(temp_r0, s8 *, 0x88) = (s8) (temp_r1_2 - 2);
                } else {
                    native_fn_02048a6c(temp_r0, 0, M2C_FIELD(temp_r0, s16 *, 0x8E));
                    temp_r1_3 = M2C_FIELD(temp_r0, s32 *, 0x84);
                    if ((s32) M2C_FIELD(temp_r0, s32 *, 0x70) >= temp_r1_3) {
                        M2C_FIELD(temp_r0, s32 *, 0x70) = temp_r1_3;
                        M2C_FIELD(temp_r0, s16 *, 0x8E) = 0;
                    } else {
                        M2C_FIELD(temp_r0, s16 *, 0x8E) = (s16) (M2C_FIELD(temp_r0, s16 *, 0x8E) + 1);
                    }
                }
            }
            var_r7 += 1;
        } while ((u32) var_r7 < (u32) M2C_FIELD(arg0, u8 *, 0x22));
    }
    if ((s32) M2C_FIELD(arg0, s16 *, 0x26) < 0) {
        return 1U;
    }
    return 0U;
}
