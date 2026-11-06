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
extern u32 native_fn_01ff8580();
extern u32 native_fn_01ff8604();
extern u32 native_fn_02041538();
extern u32 native_fn_0206258c();
extern u32 native_fn_02063b40();
extern u32 native_fn_020642cc();
extern u32 native_fn_020c40f4();
extern u32 native_fn_020cf43c();
extern u32 native_fn_020cf44c();
extern u32 native_fn_ov005_021dd608();
extern u32 native_fn_ov005_021dd798();
extern u32 native_fn_ov005_021ddf24();
extern u32 native_fn_ov005_021df3ac();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0938();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0a90();
extern u32 native_fn_ov005_021e0d88();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e5d40();
typedef struct {
    u8 unknown_0[0x38];
    s32 field_38;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e1cfc(void) {
    u16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r0_3;

    temp_r0_3 = native_fn_ov005_021e0938(1, 0x11);
    if (temp_r0_3 == 1) {
        return temp_r0_3;
    }
    native_fn_ov005_021e0d88();
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 2) {
        native_fn_ov005_021e1048(0x53);
        native_fn_ov005_021e155c(0);
        return native_fn_ov005_021e026c(4, 2, 0, 1, 0, 0);
    }
    temp_r0_2 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0_2 & 1)) {
        return (u32) temp_r0_2;
    }
    temp_r0 = native_fn_ov005_021e0a90();
    switch (temp_r0) {
    default:
        return temp_r0;
    case 0:
        native_fn_ov005_021e1048(0x52);
        native_fn_ov005_021e155c(3);
        native_fn_ov005_021e0730(0x13, 2, 0x1E);
        native_fn_01ff8604(0);
        native_fn_01ff8580(1);
        return native_fn_ov005_021ddf24();
    case 2:
        if (native_fn_02063b40(0x11D) == 0) {
            native_fn_ov005_021e1048(0x54);
            native_fn_ov005_021e0730(0x13, 2, 0x31);
            return native_fn_ov005_021e155c(2);
        }
    case 1:
        native_fn_ov005_021e5d40();
        native_fn_ov005_021e1048(0x52);
        if (native_fn_ov005_021e0a90() == 1) {
            native_fn_020642cc(0x2A);
        } else {
            native_fn_020642cc(0x2B);
        }
        native_data_ov005_021ed438.field_38 = 3;
        native_fn_ov005_021e155c(0x3D);
        native_fn_02041538(1, 2, 0xA);
        native_fn_ov005_021dd798();
        native_fn_0206258c(0);
        native_fn_020c40f4(1);
        native_fn_020cf44c(9);
        native_fn_020cf43c(3);
        native_fn_ov005_021df3ac(0x10);
        return native_fn_ov005_021dd608();
    }
}
