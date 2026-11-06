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
extern u32 native_fn_0205e7a8(u32 arg0, u32 arg1);
extern u32 native_fn_02062aa0(void);
extern u32 native_fn_0206a06c(u32);
extern u32 native_fn_0206bc80(u32 *,u8 *);
extern u32 native_fn_0206c130(void);
extern u32 native_fn_0206dcd0(u32 arg0);
extern u32 native_fn_020c48bc(void);
extern u32 native_fn_020c48d0(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_020c48e8(u32 arg0);
extern u32 native_fn_020c957c(u32 arg0);
extern u8 native_data_021d6384[];
extern u8 native_data_021d63c8[];

u32 native_main_020c8b18(s32 *arg0) {
    u8 sp4[12];
    u8 sp0[4];
    s8 var_r4;

    var_r4 = M2C_FIELD(native_data_021d63c8, s8 *, 0x10);
    *arg0 = 0;
    switch (M2C_FIELD(native_data_021d63c8, s8 *, 0x10)) {
    default:
        break;
    case 0:
        if (native_fn_02062aa0() == 0) {
            native_fn_0205e7a8(-1U, 0x54U);
        } else {
            native_fn_0205e7a8(-1U, 0x53U);
            M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
        }
        break;
    case 1:
        if (native_fn_0206a06c(1U) != 0) {
            native_fn_0206bc80((u32 *)sp4, sp0);
            if (M2C_FIELD(native_data_021d6384, u8 *, 6) != 0) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
                native_fn_020c48bc();
                native_fn_020c48d0(9U, 1U, 0x1AU);
                native_fn_020c48e8(-1U);
            } else if (M2C_FIELD(native_data_021d6384, u8 *, 1) == 1) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
            } else {
                var_r4 = 0;
            }
        }
        break;
    case 2:
        native_fn_0205e7a8(-1U, 0x53U);
        if (M2C_FIELD(native_data_021d6384, u8 *, 1) == 3) {
            M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
        } else {
            var_r4 = 0;
        }
        break;
    case 3:
        native_fn_0205e7a8(-1U, 0x53U);
        var_r4 = 2;
        break;
    case 5:
        native_fn_0205e7a8(-1U, 0x53U);
        native_fn_020c957c(0U);
        var_r4 = 3;
        break;
    case 6:
    case 7:
        if (native_fn_0206c130() != 0) {
            native_fn_0205e7a8(-1U, 0x53U);
        } else {
            native_fn_0205e7a8(-1U, 0x55U);
            native_fn_0206dcd0(0U);
        }
        if (native_fn_0206a06c(0U) != 0) {
            var_r4 = 0x7F;
        }
        break;
    case 9:
        var_r4 = 0;
        break;
    }
    return (u32) var_r4;
}
