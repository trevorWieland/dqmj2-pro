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
extern u32 native_fn_02048034();
extern u32 native_fn_020653c0();
extern u32 native_fn_020bf014();
extern u32 native_fn_020bf084();
extern u32 native_fn_020bf148();
extern u32 native_fn_020bf218();
extern u32 native_fn_ov005_021e0040();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0708();
extern u32 native_fn_ov005_021e0724();
extern u32 native_fn_ov005_021e0938();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0a90();
extern u32 native_fn_ov005_021e0d88();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e6d64();
extern u8 native_data_ov005_021e7764[];
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x13];
    s32 field_18;
    u8 unknown_1c[0x48];
    s32 field_64;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
extern u8 native_data_ov005_021edaf4[];
u32 native_ov005_021e2640(void) {
    u16 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r4;

    temp_r0_2 = native_fn_ov005_021e0938(1, 6);
    if (temp_r0_2 == 1) {
        return temp_r0_2;
    }
    native_fn_ov005_021e0d88();
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 1) {
        temp_r0_3 = native_fn_ov005_021e0a90();
        switch (temp_r0_3) {
        case 0:
            native_fn_02008e0c(native_fn_020bf014(native_data_ov005_021ed438.field_4), (u32) native_data_ov005_021edaf4, 0x268);
            native_fn_020bf148(native_data_ov005_021ed438.field_4);
            *(u32 *)native_data_ov005_021e7764 = 0x57;
            native_fn_ov005_021e155c(0x12);
            native_data_ov005_021ed438.field_18 = 0;
            break;
        case 1:
            if ((u32) M2C_FIELD((void *) native_fn_020bf014(native_data_ov005_021ed438.field_4), u8 *, 0xAF) >= 7U) {
                native_fn_ov005_021e1048(0x54);
            } else {
                native_fn_020653c0(1);
                native_fn_ov005_021e1048(0x52);
                temp_r4 = native_fn_020bf014(native_data_ov005_021ed438.field_4);
                native_fn_02008e0c(temp_r4, native_fn_020bf218(), 0x268);
                native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
                native_fn_ov005_021e0708(0x13, 2, 0xE);
                native_fn_ov005_021e155c(0x35);
                native_data_ov005_021ed438.field_64 = 0xD;
            }
            break;
        case 2:
            native_fn_ov005_021e6d64();
            native_fn_ov005_021e0708(0x13, 2, 0x1A);
            native_fn_ov005_021e0724(1);
            native_fn_ov005_021e155c(0xE);
            native_fn_ov005_021e0040();
            native_fn_ov005_021e1048(0x52);
            break;
        }
    }
    temp_r0 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_ov005_021e1048(0x53);
    native_fn_ov005_021e155c(0xC);
    native_data_ov005_021ed438.field_18 = 1;
    native_fn_ov005_021e026c(native_fn_020bf084(), native_data_ov005_021ed438.field_4, 0, 1, 0, 0);
    return native_fn_ov005_021e0040();
}
