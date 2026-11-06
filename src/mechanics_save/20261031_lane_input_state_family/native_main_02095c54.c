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
extern u32 native_fn_02089e90(void);
extern void native_fn_02094790(u32);
u32 native_main_02095c54(void *arg0, s32 arg1) {
    u8 var_r0;
    u32 temp_r1;
    s32 var_r4;

    var_r4 = arg1;
    if (var_r4 == 0x11) {
        return (u32) var_r4;
    }
    var_r0 = 0;
    temp_r1 = M2C_FIELD(arg0, u8 *, 0xD12);
    if (temp_r1 > (u32)var_r0) {
loop_4:
        if (M2C_FIELD((arg0 + (var_r0 * 4)), u8 *, 0x444) != 0) {
            var_r0 += 1;
            if ((u32) var_r0 < (u32) temp_r1) {
                goto loop_4;
            }
        }
    }
    if (var_r4 == 6) {
        if (temp_r1 == var_r0) {
            if (var_r0 == 0) {
                native_fn_02094790(5);
            } else {
                native_fn_02094790(6);
            }
            return 0x11U;
        }
        goto block_18;
    }
    if (temp_r1 == 0) {
        return (u32) var_r4;
    }
    if (temp_r1 == var_r0) {
        return (u32) var_r4;
    }
    if ((u32) M2C_FIELD((arg0 + (var_r0 * 4)), u8 *, 0x446) < 0x14U) {
        return (u32) var_r4;
    }
block_18:
    M2C_FIELD(arg0, u8 *, 0xD13) = var_r0;
    if (native_fn_02089e90() != 1) {
        M2C_FIELD(arg0, u8 *, 0xD0E) = (u8)var_r4;
        var_r4 = 7;
    }
    return (u32) var_r4;
}
