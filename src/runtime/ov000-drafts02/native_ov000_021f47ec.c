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
extern u32 native_fn_01ffb500();
extern u32 native_fn_01ffb50c();
extern u32 native_fn_020894bc();
extern u32 native_fn_020894c8();
extern u32 native_fn_020894d4();
void native_ov000_021f47ec(s32 arg0) {
    s32 var_r0;
    s32 var_r0_2;
    s32 var_r0_3;
    s32 var_r0_4;
    s32 temp_r4;
    u16 temp_r6;

    temp_r4 = *(s32 *) native_fn_020894bc();
    if (arg0 & 1) {
        temp_r6 = *(u16 *) native_fn_01ffb500();
        if (temp_r6 == 0xFF) {
            native_fn_01ffb50c(8, 0x10, 2, 5U, 0);
        } else if (*(u16 *) native_fn_01ffb500() == 0xC0) {
            native_fn_01ffb50c(8, 0xF, 0, 0xDU, 0);
        } else if (*(u16 *) native_fn_01ffb500() == 0x80) {
            native_fn_01ffb50c(8, 0xF, 0, 0xCU, 0);
        } else if ((u32) temp_r6 < 0x10U) {
            native_fn_01ffb50c(8, 0x10, 4, (u16) (temp_r6 + 1), 0);
        } else {
            native_fn_01ffb50c(8, 0x10, 0xD, (u16) ((u16) (temp_r6 - 0x10) + 0xA), 0);
        }
    }
    if (!(arg0 & 2)) {
        return;
    }
    if (*(u16 *) native_fn_01ffb500() == 0xFF) {
        native_fn_01ffb50c(0xB, 0x10, 2, 5U, 0);
        native_fn_01ffb50c(0xE, 0x10, 2, 5U, 0);
        native_fn_01ffb50c(0x11, 0x10, 2, 5U, 0);
        native_fn_01ffb50c(0x17, 0x10, 2, 5U, 0);
        native_fn_01ffb50c(0x14, 0x10, 2, 5U, 0);
        native_fn_01ffb50c(0x1A, 0x10, 2, 5U, 0);
        return;
    }
    var_r0 = 0;
    if (temp_r4 & 0x800000) {
        var_r0 = 1;
    }
    if (temp_r4 & 0x01000000) {
        var_r0 = 2;
    }
    native_fn_01ffb50c(0xB, 0x10, 4, (u16) (var_r0 + 0x23), 0);
    var_r0_2 = 0;
    if (temp_r4 & 0x02000000) {
        var_r0_2 = 1;
    }
    native_fn_01ffb50c(0xE, 0x10, 4, (u16) (var_r0_2 + 0x26), 0);
    var_r0_3 = 0;
    if (temp_r4 & 1) {
        var_r0_3 = 1;
    }
    if (temp_r4 & 0x04000000) {
        var_r0_3 = 2;
    }
    native_fn_01ffb50c(0x11, 0x10, 4, (u16) (var_r0_3 + 0x37), 0);
    var_r0_4 = 0;
    if (temp_r4 & 0x08000000) {
        var_r0_4 = 1;
    }
    if (temp_r4 & 0x10000000) {
        var_r0_4 = 2;
    }
    native_fn_01ffb50c(0x14, 0x10, 4, (u16) (var_r0_4 + 0x2D), 0);
    native_fn_01ffb50c(0x17, 0x10, 4, (u16) (*(s32 *) native_fn_020894d4() + 0x2A), 0);
    native_fn_01ffb50c(0x1A, 0x10, 4, (u16) (*(s32 *) native_fn_020894c8() + 0x31), 0);
}
