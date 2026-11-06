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
extern u32 native_fn_0202a634();
extern u32 native_fn_020414c8();
extern u32 native_fn_02041538();
extern u32 native_fn_0204157c();
extern u32 native_fn_02041814();
extern u32 native_fn_02041908();
extern u32 native_fn_02045680();
extern u32 native_fn_02046af4();
extern u32 native_fn_02049ae4();
extern u32 native_fn_02049c90();
extern u32 native_fn_02049d50();
extern u32 native_fn_02049e28();
extern u32 native_fn_02049f14();
extern u32 native_fn_02049f24();
extern u32 native_fn_0205dc70();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02068f60();
extern u32 native_fn_02085200();
extern u32 native_fn_020853c8();
extern u32 native_fn_02086b14();
extern u8 native_data_021c9698[];
typedef struct {
    u8 field_0;
    u8 field_1;
    u8 unknown_2[0x1];
    u8 field_3;
    u8 field_4;
    u8 unknown_5[0x2];
    u8 field_7;
    u8 field_8;
    u8 unknown_9[0x1];
    u16 field_a;
    u16 field_c;
    u8 unknown_e[0x16];
    s32 field_24;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
extern u8 native_data_ov001_0223df1c[];
u32 native_ov001_0220a1c8(void) {
    void *temp_r2;
    u32 var_r4;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r6_2;

    var_r4 = 3;
    temp_r6 = native_fn_0202a634();
    temp_r5 = native_fn_02049ae4();
    switch ((s32) native_data_ov001_0223def8.field_3) {
    case 0x0:
        native_fn_020414c8(0x1E);
        native_fn_02041538(1, 2, 4);
        native_fn_0204157c(0xA);
        native_data_ov001_0223def8.field_24 = 1;
        native_fn_02049c90(0, native_data_ov001_0223df1c, -1);
        if (native_data_ov001_0223def8.field_4 != 0xFF) {
            temp_r6_2 = native_fn_02049f24();
            native_fn_02046af4(native_data_021c9698, native_fn_0205dc70(native_data_ov001_0223def8.field_4, native_data_ov001_0223def8.field_0, native_data_ov001_0223def8.field_a), 0x1F, 0, temp_r6_2, 0xFF);
            native_fn_02049f14(temp_r6_2);
            native_fn_020853c8(M2C_FIELD(temp_r5, void **, 4), M2C_FIELD(temp_r5, s32 *, 0));
        }
        native_fn_02049e28(native_data_ov001_0223def8.field_8, native_data_ov001_0223def8.field_1, native_data_ov001_0223def8.field_c);
        temp_r2 = M2C_FIELD(temp_r5, void **, 4);
        M2C_FIELD(temp_r2, s32 *, 0x18) = (s32) (M2C_FIELD(temp_r2, s32 *, 0x18) | 2);
        native_fn_02086b14(M2C_FIELD(temp_r5, void **, 4), 0xA);
        if (native_data_ov001_0223def8.field_7 != 0) {
            native_data_ov001_0223def8.field_7 = 0U;
        } else {
            native_fn_0205e7a8(-1, 0x57);
        }
        native_data_ov001_0223def8.field_3 = 0x14U;
        break;
    case 0x14:
        if (native_fn_02041814() != 1) {
            native_data_ov001_0223def8.field_3 = 0x28U;
        }
        break;
    case 0x28:
        if (M2C_FIELD(temp_r6, u16 *, 2) & 0xFF7) {
            native_fn_02041538(0, 2, 4);
            native_fn_02041908(4, 0xA);
            native_fn_02045680(0);
            native_fn_02049d50();
            native_data_ov001_0223def8.field_24 = 0x20;
            native_data_ov001_0223def8.field_3 = 0x3CU;
        }
        break;
    case 0x3C:
        if (native_fn_02041814() != 1) {
            native_fn_020414c8(0x3F);
            var_r4 = 1;
            native_data_ov001_0223def8.field_3 = 0U;
            native_fn_02068f60(1);
        }
        break;
    }
    native_fn_02085200();
    return var_r4;
}
