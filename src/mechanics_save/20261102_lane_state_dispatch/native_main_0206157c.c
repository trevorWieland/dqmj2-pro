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
extern u32 native_fn_020406b8(void);
extern u32 native_fn_02041800(void);
extern u32 native_fn_02041814(void);
extern void native_fn_02045654(s32 arg0);
extern u32 native_fn_02060d94();
extern u32 native_fn_02060e54();
extern u32 native_fn_02060f14();
extern u32 native_fn_0206100c();
extern u32 native_fn_020612a8(s8 arg0);
extern u32 native_fn_02061470();
extern u32 native_fn_02061898();
extern u32 native_fn_02061950(s32 arg0);
extern u32 native_fn_020619b0();
extern u32 native_fn_02061ba8(void);
extern u32 native_fn_02062134(s8 arg0);
extern u32 native_fn_02062144();
extern u32 native_fn_02062368(s8 arg0);
extern u32 native_fn_020675c8(u8 arg0);
extern u8 native_data_020dac94[];
extern u8 native_data_020dac98[];
extern u8 native_data_021b9bc8[];
extern u8 native_data_021b9bd0[];
extern u8 native_data_021b9bd4[];

u32 native_main_0206157c(void) {
    u32 (*temp_r0_2)(void);
    u32 (*temp_r0)(void);
    s8 var_r2;
    u32 temp_r0_3;
    u32 var_r4;

    var_r4 = 0;
    switch (M2C_FIELD(native_data_021b9bd4, s8 *, 0x268)) {
    default:
        break;
    case 0:
        if ((M2C_FIELD(native_data_021b9bd4, s8 *, 0x2A3) != 0) || ((native_fn_02041800() != 1) && (native_fn_02041814() != 1))) {
            M2C_FIELD(native_data_021b9bd4, s8 *, 0x268) = 1;
        }
        break;
    case 1:
        native_fn_02061470();
        M2C_FIELD(native_data_021b9bd4, s8 *, 0x268) = 2;
        break;
    case 2:
        native_fn_02061950((s32) M2C_FIELD(native_data_021b9bd4, s8 *, 0x269));
        native_fn_02061ba8();
        M2C_FIELD(native_data_021b9bd4, s8 *, 0x268) = 3;
        break;
    case 3:
        temp_r0 = M2C_FIELD(native_data_020dac94, u32 (**)(void), M2C_FIELD(native_data_021b9bd4, s8 *, 0x269) * 0xC);
        if (temp_r0 == NULL) {
            native_fn_020619b0(0);
        } else if (temp_r0() != 0) {
            native_fn_020619b0(M2C_FIELD(native_data_021b9bd4, s8 *, 0x26C));
        } else if (native_fn_020406b8() == 0) {
            temp_r0_2 = M2C_FIELD(native_data_020dac98, u32 (**)(void), M2C_FIELD(native_data_021b9bd4, s8 *, 0x269) * 0xC);
            if (temp_r0_2 != NULL) {
                temp_r0_2();
            }
            native_fn_020675c8((u32) M2C_FIELD(native_data_021b9bc8, u8 *, 2));
            native_fn_02045654((u32) M2C_FIELD(native_data_021b9bd0, u8 *, 0));
            native_fn_02045654((u32) M2C_FIELD(native_data_021b9bd0, u8 *, 1));
            native_fn_02045654((u32) M2C_FIELD(native_data_021b9bd0, u8 *, 2));
            M2C_FIELD(native_data_021b9bd4, s8 *, 0x268) = 5;
        }
        break;
    case 4: {
        s32 var_r5;
        var_r5 = 0;
        if ((s32) M2C_FIELD(native_data_021b9bc8, s8 *, 3) <= -1) {
            if (M2C_FIELD(native_data_021b9bc8, s8 *, 3) != -1) {
                goto block_39;
            }
        } else {
            temp_r0_3 = M2C_FIELD(native_data_021b9bc8, s8 *, 3) - 0x78;
            switch (temp_r0_3) {
            case 0:
            case 1:
                native_fn_02060d94();
                M2C_FIELD(native_data_021b9bc8, s8 *, 3) = -1;
                break;
            case 2:
                native_fn_02060e54();
                M2C_FIELD(native_data_021b9bc8, s8 *, 3) = -1;
                break;
            case 3:
                native_fn_02060f14();
                M2C_FIELD(native_data_021b9bc8, s8 *, 3) = -1;
                break;
            case 5:
                native_fn_02060e54();
                M2C_FIELD(native_data_021b9bc8, s8 *, 3) = -1;
                break;
            default:
            case 4:
block_39:
                native_fn_0206100c();
                M2C_FIELD(native_data_021b9bc8, s8 *, 3) = -1;
                break;
            }
        }
        if (M2C_FIELD(native_data_021b9bd4, s8 *, 0x2A2) == 0) {
            if (M2C_FIELD(native_data_021b9bd4, s8 *, 0x26E) == 1) {
                if ((s32) M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) > 0) {
                    M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) = (s8) (M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) - 6);
                    if ((s32) M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) < 0) {
                        M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) = 0;
                    }
                } else {
                    var_r5 = 1;
                    native_fn_02062134(0U);
                }
            } else if ((s32) M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) < 0x20) {
                M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) = (s8) (M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) + 6);
                if ((s32) M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) > 0x20) {
                    M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) = 0x20;
                }
            } else {
                var_r5 = 1;
                native_fn_02062134(0U);
            }
        } else {
            var_r5 = 1;
            if (M2C_FIELD(native_data_021b9bd4, s8 *, 0x26E) == 1) {
                var_r2 = 0;
            } else {
                var_r2 = 0x20;
            }
            M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F) = var_r2;
            native_fn_02062134(0U);
            native_fn_020612a8(0U);
        }
        native_fn_02062144(M2C_FIELD(native_data_021b9bd4, s8 *, 0x26F), M2C_FIELD(native_data_021b9bd4, s8 *, 0x26E));
        if (var_r5 != 0) {
            native_fn_02062368(0U);
            M2C_FIELD(native_data_021b9bd4, s8 *, 0x268) = 2;
        }
        break;
    }
    case 5:
        if (native_fn_02041800() != 1) {
            native_fn_02061898();
            var_r4 = 1;
        }
        break;
    }
    return var_r4;
}
