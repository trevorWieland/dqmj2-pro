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
extern u32 native_fn_02062a10();
extern u32 native_fn_02068bd4();
extern u32 native_fn_02068c14();
extern u32 native_fn_020692b0();
extern u32 native_fn_0206c1a8();
extern u32 native_fn_020bfb10();
extern u32 native_fn_020bfe70();
extern u32 native_fn_020c01f0();
extern u32 native_fn_020c1888();
extern u32 native_fn_020c3828();
extern u32 native_fn_020c3904();
typedef struct {
    u8 unknown_0[0x18];
    s32 field_18;
} Record_native_data_ov003_021e0d18;
extern Record_native_data_ov003_021e0d18 native_data_ov003_021e0d18;
u32 native_ov003_021dfe30(void) {
    u8 *temp_r0;
    u8 *temp_r0_2;
    u8 var_r7;
    u8 var_r8;
    u8 var_r8_2;
    u8 var_r9;

    native_fn_02068bd4(native_data_ov003_021e0d18.field_18);
    native_fn_020c1888(0x12);
    var_r8 = 0;
    var_r7 = 0;
    do {
        native_fn_020c3828(var_r7);
        temp_r0 = native_fn_02062a10();
        if (temp_r0 != NULL) {
            native_fn_020692b0(M2C_FIELD(temp_r0, s32 *, 0x14), 0, 0, var_r8, 0, 0x12, 0xF);
            var_r8 += native_fn_0206c1a8(M2C_FIELD(temp_r0, s16 *, 0x18)) + 1;
        }
        var_r7 += 1;
    } while ((u32) var_r7 < 3U);
    var_r8_2 = 0;
    var_r9 = 0;
    do {
        native_fn_020c3904(var_r9);
        temp_r0_2 = native_fn_02062a10();
        if (temp_r0_2 != NULL) {
            native_fn_020692b0(M2C_FIELD(temp_r0_2, s32 *, 0x14), 1, 0, var_r8_2, 0, 0x12, 0xF);
            var_r8_2 += native_fn_0206c1a8(M2C_FIELD(temp_r0_2, s16 *, 0x18)) + 1;
        }
        var_r9 += 1;
    } while ((u32) var_r9 < 3U);
    native_fn_020bfb10(0);
    native_fn_020c01f0();
    native_fn_020bfe70(native_data_ov003_021e0d18.field_18);
    return native_fn_02068c14(2, 0x24, 0x20, 1);
}
