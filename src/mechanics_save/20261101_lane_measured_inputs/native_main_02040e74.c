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
extern u32 native_fn_0202acec(u32, u32, const void *, u32);
extern u32 native_fn_0203d348();
u32 native_main_02040e74(void *arg0, u32 arg1) {
    u32 firstHandle;
    u32 thirdHandle;
    void *temp_r1;
    void *temp_r1_2;
    void *temp_r1_3;
    void *temp_r2;
    void *temp_r2_2;
    void *temp_r3;
    u32 var_r4;
    u32 temp_r5_2;
    void *temp_r5;
    u32 temp_r6;

    var_r4 = 0;
    firstHandle = M2C_FIELD(arg0, u32 *, 0x4C);
    if (firstHandle != 0) {
        temp_r5 = M2C_FIELD(arg0, void **, 0x3C);
        if (native_fn_0202acec(0, (u32) (M2C_FIELD(arg0, u32 *, 0x40) << 0x10) >> 0xD, temp_r5 + M2C_FIELD(temp_r5, s32 *, 0x14), firstHandle) != 0) {
            temp_r1 = M2C_FIELD(arg0, void **, 0x3C);
            var_r4 |= 1;
            M2C_FIELD(temp_r1, u16 *, 0x10) = (u16) (M2C_FIELD(temp_r1, u16 *, 0x10) | 1);
        }
    }
    temp_r6 = M2C_FIELD(arg0, u32 *, 0x50);
    if (temp_r6 != 0) {
        temp_r2 = M2C_FIELD(arg0, void **, 0x3C);
        temp_r5_2 = (u32) (M2C_FIELD(arg0, u32 *, 0x44) << 0x10) >> 0xD;
        if (native_fn_0202acec(0, temp_r5_2, temp_r2 + M2C_FIELD(temp_r2, s32 *, 0x24), temp_r6) != 0) {
            temp_r3 = M2C_FIELD(arg0, void **, 0x3C);
            if (native_fn_0202acec(0, ((u32) (temp_r5_2 & 0x1FFFF) >> 1) + 0x20000 + ((u32) (temp_r5_2 & 0x40000) >> 2), temp_r3 + M2C_FIELD(temp_r3, s32 *, 0x28), temp_r6 >> 1) != 0) {
                temp_r1_2 = M2C_FIELD(arg0, void **, 0x3C);
                var_r4 |= 2;
                M2C_FIELD(temp_r1_2, u16 *, 0x20) = (u16) (M2C_FIELD(temp_r1_2, u16 *, 0x20) | 1);
            }
        }
    }
    thirdHandle = M2C_FIELD(arg0, u32 *, 0x54);
    if (thirdHandle != 0) {
        temp_r2_2 = M2C_FIELD(arg0, void **, 0x3C);
        if (native_fn_0202acec(1, (u32) (M2C_FIELD(arg0, u32 *, 0x48) << 0x10) >> 0xD, temp_r2_2 + M2C_FIELD(temp_r2_2, s32 *, 0x38), thirdHandle) != 0) {
            temp_r1_3 = M2C_FIELD(arg0, void **, 0x3C);
            var_r4 |= 4;
            M2C_FIELD(temp_r1_3, u16 *, 0x32) = (u16) (M2C_FIELD(temp_r1_3, u16 *, 0x32) | 1);
        }
    }
    native_fn_0203d348(arg1);
    return var_r4;
}
