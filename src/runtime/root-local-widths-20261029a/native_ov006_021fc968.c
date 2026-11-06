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
extern u32 native_fn_ov006_021ff0bc();
extern u32 native_fn_ov006_02202eb0();
extern u32 native_fn_ov006_02202f54();
extern u32 native_fn_ov006_02203058();
extern u8 native_data_ov006_0220b808[];
extern u8 native_data_ov006_0220b82a[];
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov006_0221c10c;
extern Record_native_data_ov006_0221c10c native_data_ov006_0221c10c;
u32 native_ov006_021fc968(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    s32 temp_r3;
    s32 var_r4;
    s32 var_r5;
    u8 *var_r7;
    u8 *sp4;
    u32 sp0;

    var_r7 = native_data_ov006_0220b82a;
    var_r5 = 0;
    var_r4 = 0;
    sp4 = native_data_ov006_0220b82a;
    do {
        temp_r0_2 = native_fn_ov006_021ff0bc(var_r5);
        sp0 = temp_r0_2;
        if (temp_r0_2 == 0xFF) {
            sp0 = 3;
        } else {
            M2C_FIELD((native_data_ov006_0221c10c.field_4 + var_r4), u32 *, 0x10) = native_fn_ov006_02203058(0, 0x11U, 1);
            temp_r3 = (var_r5 + 3) * 4;
            native_fn_ov006_02202eb0(M2C_FIELD((native_data_ov006_0221c10c.field_4 + var_r4), s32 *, 0x10), -1, *(u16 *)(sp4 + temp_r3), M2C_FIELD((sp4 + temp_r3), u16 *, 2));
            native_fn_ov006_02202f54(M2C_FIELD((native_data_ov006_0221c10c.field_4 + var_r4), s32 *, 0x10), -1, 3);
        }
        M2C_FIELD((native_data_ov006_0221c10c.field_4 + var_r4), u32 *, 4) = native_fn_ov006_02203058(0, native_data_ov006_0220b808[sp0], 1);
        native_fn_ov006_02202eb0(M2C_FIELD((native_data_ov006_0221c10c.field_4 + var_r4), s32 *, 4), -1, M2C_FIELD(var_r7, u16 *, 0), M2C_FIELD(var_r7, u16 *, 2));
        temp_r0 = native_fn_ov006_02202f54(M2C_FIELD((native_data_ov006_0221c10c.field_4 + var_r4), s32 *, 4), -1, 3);
        var_r5 += 1;
        var_r4 += 4;
        var_r7 += 4;
    } while (var_r5 < 3);
    return temp_r0;
}
