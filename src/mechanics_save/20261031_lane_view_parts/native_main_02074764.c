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
extern u32 native_fn_020496b0(void *);
extern u32 native_fn_0204b138(void *,u32,u32);
extern u8 *ov000_display_context_02215698(void);
extern u32 native_data_021c5a24;
extern u8 native_data_021c5a30[];
extern u8 native_data_021c5b20[];
u32 native_main_02074764(void) {
    u32 var_r2;
    u32 var_r2_2;
    u8 *temp_r0;
    u8 *var_r4;
    u8 temp_r0_2;

    temp_r0 = ov000_display_context_02215698();
    var_r4 = NULL;
    switch (native_data_021c5a24) {
    case 3:
        var_r4 = native_data_021c5b20;
        break;
    case 1:
        var_r4 = native_data_021c5a30;
        break;
    }
    temp_r0_2 = M2C_FIELD(temp_r0, u8 *, 0x494);
    switch (temp_r0_2) {
    default:
        break;
    case 3:
    case 4:
    case 9:
    case 10:
        if ((var_r4 != NULL) && (M2C_FIELD(var_r4, s32 *, 0xC4) != 0)) {
            if ((s32) M2C_FIELD(var_r4, s32 *, 4) > 0) {
                var_r2 = 1;
            } else {
                var_r2 = 0;
            }
            native_fn_0204b138(var_r4 + 0xA8, 0, var_r2);
            if ((s32) ((u32)M2C_FIELD(var_r4, s32 *, 4) + M2C_FIELD(var_r4, u16 *, 0xC)) < (s32) M2C_FIELD(var_r4, u16 *, 0xE)) {
                var_r2_2 = 1;
            } else {
                var_r2_2 = 0;
            }
            native_fn_0204b138(var_r4 + 0xA8, 1, var_r2_2);
            native_fn_020496b0(var_r4 + 0xA8);
        }
        break;
    }
    return 0U;
}
