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
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern u32 native_fn_0202a37c();
extern u32 native_fn_0206d230();
extern u32 native_fn_ov001_021fdbcc();
extern u32 native_fn_ov001_021fe54c();
extern u32 native_fn_ov001_021fe9b0();
extern u8 native_data_020fbae8[];
typedef struct {
    u8 unknown_0[0xc];
    s8 field_c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
typedef struct {
    u8 unknown_0[0x204];
    u32 field_204;
} Record_native_data_ov001_0223a030;
extern Record_native_data_ov001_0223a030 native_data_ov001_0223a030;
u32 native_ov001_02202b88(void) {
    u32 temp_r0;
    void *temp_r1;
    u8 var_r3;
    u32 temp_r4;

    temp_r4 = native_fn_0206d230();
    if (native_data_ov001_0223a030.field_204 == 0) {
        temp_r0 = native_fn_0202a37c(2, 0x168, 4);
        native_data_ov001_0223a030.field_204 = temp_r0;
        native_fn_02008e0c(temp_r4, temp_r0, 0x168);
    }
    var_r3 = 0;
    do {
        temp_r1 = M2C_FIELD((native_data_020fbae8 + (var_r3 * 4)), void **, 0x6C88);
        if (temp_r1 != NULL) {
            M2C_FIELD(temp_r1, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r1, s32 *, 0x7C) & ~2);
        }
        var_r3 += 1;
    } while ((u32) var_r3 < 0x80U);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x1E);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x7F);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x15);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x16);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x1F);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x20);
    native_fn_ov001_021fe54c(native_data_ov001_02239c10.field_c, 0x21);
    native_fn_ov001_021fe9b0();
    native_fn_ov001_021fdbcc();
    return native_fn_02008d78(0x07000400, 0, 0x400);
}
