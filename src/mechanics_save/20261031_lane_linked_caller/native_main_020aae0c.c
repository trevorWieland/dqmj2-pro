#define NULL ((void *)0)
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
extern u32 native_fn_020a8f14(u32);
extern u32 native_fn_020aa9b4(void **);
extern u32 native_fn_020aab70(void **);
extern u32 native_fn_020ace1c(void **,s32);
extern u32 native_fn_020add0c(void **);
extern u32 native_fn_020ade3c(void **,u32);
extern u32 native_fn_020af7f8(void **,void *);
extern u32 native_fn_020afad8(void **,void *);
extern u32 native_fn_020afb10(void **,void **,s32);
extern u32 native_fn_020b0348(void **);
extern u32 native_fn_020b27a0(void **);
u32 native_main_020aae0c(void **arg0, s32 arg1) {
    s32 temp_r0_2;
    u32 temp_r0;
    u32 var_r0;
    void *var_r1;
    s32 var_r4;
    void *temp_r6;
    void *sp4;
    u32 sp0;

    sp0 = 0;
    temp_r6 = *arg0;
    if (M2C_FIELD(temp_r6, s32 *, 0x1F4) == 1) {
        do {
            temp_r0 = native_fn_020add0c(arg0);
            sp0 = temp_r0;
            if ((temp_r0 == 0) && (arg1 != 0) && (M2C_FIELD(temp_r6, s32 *, 0x1F4) == 1)) {
                var_r4 = 1;
            } else {
                var_r4 = 0;
            }
            if (var_r4 != 0) {
                native_fn_020a8f14(0xA);
            }
        } while (var_r4 != 0);
        if ((sp0 != 0) && (native_fn_020afb10(arg0, &sp4, 1) != 0)) {
            M2C_FIELD(sp4, s32 *, 0x1C) = 4;
        }
    }
    temp_r0_2 = M2C_FIELD(temp_r6, s32 *, 0x1F4);
    if ((temp_r0_2 == 3) || (temp_r0_2 == 2) || (temp_r0_2 == 5)) {
        if (sp0 == 0) {
            sp0 = native_fn_020aab70(arg0);
        }
        if (sp0 == 0) {
            sp0 = native_fn_020b0348(arg0);
        }
    }
    if (sp0 == 0) {
        sp0 = native_fn_020b27a0(arg0);
    }
    var_r1 = M2C_FIELD(temp_r6, void **, 0x5C4);
    sp4 = var_r1;
    if (var_r1 != NULL) {
        do {
            if (M2C_FIELD(var_r1, s32 *, 0x1C) != 0) {
                native_fn_020af7f8(arg0,var_r1);
                var_r1 = sp4;
                sp4 = M2C_FIELD(var_r1, void **, 0x20);
                native_fn_020afad8(arg0,var_r1);
            } else {
                sp4 = M2C_FIELD(var_r1, void **, 0x20);
            }
            var_r1 = sp4;
        } while (var_r1 != NULL);
    }
    var_r0 = native_fn_020ace1c(arg0, arg1);
    if (var_r0 == 0) {
        if (M2C_FIELD(temp_r6, s32 *, 0x5BC) != 0) {
            native_fn_020ade3c(arg0, 0);
            native_fn_020aa9b4(arg0);
        }
        var_r0 = sp0;
    }
    return var_r0;
}
