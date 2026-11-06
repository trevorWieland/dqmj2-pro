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
extern u32 native_fn_02008e0c();
extern u32 native_fn_02026144();
u32 native_ov005_021d9de0(void *arg0, u8 *arg1, u8 **arg2) {
    void *temp_r0;
    s32 temp_r1;
    u16 temp_r2;
    void *temp_r3;
    u8 *temp_r4;
    u64 temp_r6;
    u16 temp_r7;

    temp_r4 = *arg2;
    temp_r0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x20), void **, 0xC);
    temp_r3 = M2C_FIELD(temp_r0, void **, 0x24);
    temp_r2 = M2C_FIELD(arg1, u16 *, 2);
    if (temp_r4 == 0) {
        return (u32) temp_r0;
    }
    temp_r6 = temp_r2 * 0x1FC;
    if (temp_r2 == (M2C_FIELD(temp_r3, s32 *, 0x424) - 1)) {
        temp_r7 = M2C_FIELD(temp_r3, u16 *, 0x586);
        temp_r1 = M2C_FIELD(temp_r3, s32 *, 0x420) % (s32)temp_r7;
        if (temp_r1 != 0) {
            return native_fn_02008e0c(arg1 + 4, temp_r4 + (u32)temp_r6, temp_r1);
        }
        return native_fn_02008e0c(arg1 + 4, temp_r4 + (u32)temp_r6, (s32) temp_r7);
    }
    return native_fn_02008e0c(arg1 + 4, temp_r4 + (u32)temp_r6, (s32) M2C_FIELD(temp_r3, u16 *, 0x586));
}
