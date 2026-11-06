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
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u32 native_fn_0205f210();
extern u32 native_fn_0205f6a0();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d774c();
extern u32 native_fn_ov001_021d78a4();
extern u32 native_fn_ov001_021d7e48();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021e34f0();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f13f8();
extern u32 native_fn_ov001_021f1414();
extern u32 native_fn_ov001_021f1438();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f14e4();
extern u32 native_fn_ov001_021f949c();
typedef struct {
    u8 field_0;
    u8 field_1;
    u8 unknown_2[0xa];
    u32 field_c;
    s32 field_10;
} Record_native_data_ov001_02242ba0;
extern Record_native_data_ov001_02242ba0 native_data_ov001_02242ba0;
u32 native_ov001_02215314(void) {
    s32 temp_r4;
    s32 temp_r5;
    void *temp_r0;

    if (native_data_ov001_02242ba0.field_1 == 0x0) {
        native_fn_ov001_021d7e48(0x2F);
        native_fn_ov001_021f1354(1, 0, 0x14, 0);
        native_fn_ov001_021f1414(1);
        native_fn_ov001_021f1438();
        native_fn_ov001_021f13f8(0x1E);
        native_fn_0205f6a0(1, 0x3F, 0xA);
        native_fn_ov001_021d75d4(0x2F);
        native_fn_ov001_021d94cc(1, 1);
        native_fn_ov001_021e34f0(1);
        native_data_ov001_02242ba0.field_1 = 0xAU;
        native_data_ov001_02242ba0.field_0 = 0;
    }
    else if (native_data_ov001_02242ba0.field_1 == 0xA) {
        temp_r0 = (void *) native_fn_ov001_021d7e48(0x2F);
        temp_r5 = M2C_FIELD(temp_r0, s32 *, 4);
        temp_r4 = M2C_FIELD(M2C_FIELD(temp_r0, void **, 0x30), s32 *, 4) - 1;
        if (temp_r5 == (temp_r4 - 0x32)) {
            native_fn_ov001_021d78a4(0, 0x31, 1, 1);
            native_data_ov001_02242ba0.field_c = native_fn_ov001_021f949c(0x154, 1);
        }
        if (temp_r5 == 0x76) {
            native_fn_ov001_021f14a4();
        }
        if ((temp_r5 > 0x76) && (native_fn_ov001_021f14e4() == 0)) {
            native_fn_ov001_021f1354(1, 0, 0x23, 0);
        }
        if (temp_r5 == (temp_r4 - 0x14)) {
            native_fn_020414b0(1);
            native_fn_02041510(1, 3, 0xA);
        }
        if (native_fn_ov001_021d774c(0x2F) == 0) {
            native_data_ov001_02242ba0.field_1 = 0x14U;
            native_fn_0205f6a0(1, 0x7F, 0xA);
        }
    }
    else if (native_data_ov001_02242ba0.field_1 == 0x14) {
        native_fn_ov001_021f14a4();
        native_data_ov001_02242ba0.field_1 = 0x64U;
    }
    else if (native_data_ov001_02242ba0.field_1 == 0x64) {
        if (native_fn_ov001_021f14e4() != 0) {
            native_fn_0205f210(native_data_ov001_02242ba0.field_c, 0);
            native_data_ov001_02242ba0.field_1 = 0U;
            native_data_ov001_02242ba0.field_10 = 2;
        }
    }

    return 0U;
}
