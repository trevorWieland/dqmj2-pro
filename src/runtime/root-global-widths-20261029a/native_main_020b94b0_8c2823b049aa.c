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
extern u32 native_fn_020902d0();
extern u32 native_fn_02090310();
extern u32 native_fn_0209088c();
extern u32 native_fn_020b909c();
extern u32 native_fn_020b90ec();
extern u32 native_fn_020b9100();
extern u32 native_fn_020b9868();
extern u32 native_fn_020b9898();
extern u8 native_data_020e2c48[];
extern u8 native_data_021d3028[];
u32 native_main_020b94b0(void) {
    s32 temp_r0_2;
    u16 temp_r0;
    u8 *temp_r1;
    u8 *var_r4;
    u16 var_r5;
    u8 sp0[8];

    var_r4 = native_data_020e2c48;
    var_r5 = 0xD68F;
    temp_r1 = M2C_FIELD(*(u32 *)native_data_021d3028, u8 **, 0x20);
    if (temp_r1 != NULL) {
        var_r4 = temp_r1;
    } else if (native_fn_020b9868(*(u32 *)native_data_021d3028 + 0x48) != 0) {
        var_r4 = *(u32 *)native_data_021d3028 + 0x48;
    }
    temp_r0 = M2C_FIELD(*(u32 *)native_data_021d3028, u16 *, 0x24);
    if (temp_r0 != 0) {
        var_r5 = temp_r0;
    }
    if (M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 4) == 2) {
        return native_fn_020b90ec(5);
    }
    if (native_fn_020b9898(var_r4, var_r5, &sp0) == 0) {
        native_fn_020b909c(5, -0x1E);
        return native_fn_020b9100(5);
    }
    if (M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 4) == 2) {
        return native_fn_020b90ec(5);
    }
    temp_r0_2 = (s32) native_fn_020902d0(2, 1, 0);
    if (temp_r0_2 < 0) {
        native_fn_020b909c(5, -0x32);
        return native_fn_020b9100(5);
    }
    M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 0x1B8) = temp_r0_2;
    if (M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 4) == 2) {
        return native_fn_020b90ec(5);
    }
    if ((s32) native_fn_0209088c(M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 0x1B8), *(u32 *)native_data_021d3028 + 0x1D4) < 0) {
        native_fn_020b909c(5, -0x32);
        return native_fn_020b9100(5);
    }
    if (M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 4) == 2) {
        return native_fn_020b90ec(5);
    }
    if ((s32) native_fn_02090310(M2C_FIELD(*(u32 *)native_data_021d3028, s32 *, 0x1B8), &sp0) < 0) {
        native_fn_020b909c(6, -0x3C);
        return native_fn_020b9100(5);
    }
    return native_fn_020b90ec(6);
}
