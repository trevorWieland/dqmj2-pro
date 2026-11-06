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
extern u32 native_fn_02048094();
extern u32 native_fn_02049ae4();
extern u32 native_fn_0204b380();
extern u32 native_fn_0205f35c();
extern u32 native_fn_02063b18();
extern u32 native_fn_02085320();
extern u32 native_fn_02086b38();
extern u32 native_fn_ov000_021e7b9c();
extern u32 native_fn_ov000_021f7f7c();
extern u32 native_fn_ov000_021f85c8();
extern u32 native_fn_ov000_021fb000();
extern u32 native_fn_ov000_021fb030();
extern u32 native_fn_ov000_021fbcb8();
extern u32 native_fn_ov000_021fbdec();
extern u32 native_fn_ov000_02215698();
extern u32 native_fn_ov000_0221767c();
extern u32 native_fn_ov000_02217c68();
extern u32 native_fn_ov000_02217c9c();
typedef struct {
    u8 field_0;
    u8 field_1;
} Record_native_data_ov000_0222f42c;
extern Record_native_data_ov000_0222f42c native_data_ov000_0222f42c;
typedef struct {
    u8 field_0;
    u8 field_1;
} Record_native_data_ov000_0223716c;
extern Record_native_data_ov000_0223716c native_data_ov000_0223716c;
u32 native_ov000_021faba8(void) {
    u16 temp_r0_3;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;
    u32 var_r5;
    u8 var_r1;

    temp_r4 = native_fn_ov000_02215698();
    temp_r0 = native_fn_0202a634();
    var_r5 = 0;
    switch (native_data_ov000_0223716c.field_1) {
    default:
        break;
    case 0:
        native_data_ov000_0222f42c.field_0 = 0;
        if (native_data_ov000_0222f42c.field_1 == 6) {
            native_data_ov000_0223716c.field_1 = 2U;
        } else {
            temp_r0_2 = native_fn_ov000_02217c68(5, 6, 1, 1, 1, -1);
            native_fn_02085320(temp_r0_2, 0, 1);
            native_fn_02085320(temp_r0_2, 1, 0xE);
            native_fn_02048094(native_fn_02063b18(0x3D), 0);
            native_fn_ov000_021e7b9c(0x52);
            native_fn_0204b380(temp_r4 + 0x10, 0);
            native_data_ov000_0223716c.field_1 = 1U;
        }
        break;
    case 1:
        temp_r0_3 = M2C_FIELD(temp_r0, u16 *, 2);
        if (temp_r0_3 & 1) {
            if (native_fn_02086b38(M2C_FIELD((void *) native_fn_02049ae4(), s32 *, 4)) == 0) {
                native_fn_ov000_02217c9c(0);
                native_data_ov000_0223716c.field_1 = 2U;
            } else {
                native_fn_ov000_021e7b9c(0x52);
                native_data_ov000_0223716c.field_1 = 4U;
            }
        } else if (temp_r0_3 & 2) {
            native_data_ov000_0222f42c.field_0 = 1;
            native_fn_ov000_021e7b9c(0x53);
            native_data_ov000_0223716c.field_1 = 4U;
        }
        break;
    case 2:
        native_data_ov000_0223716c.field_0 = 0;
        if (native_data_ov000_0222f42c.field_1 == 6) {
            native_fn_ov000_021fb000();
        } else {
            native_fn_ov000_021fb030();
            native_data_ov000_0223716c.field_0 = 1;
        }
        native_fn_ov000_021f7f7c(1);
        native_fn_ov000_0221767c();
        native_fn_ov000_021f85c8();
        if (native_data_ov000_0223716c.field_0 != 0) {
            var_r1 = 2;
        } else {
            var_r1 = 3;
        }
        native_data_ov000_0222f42c.field_0 = var_r1;
        if (native_data_ov000_0222f42c.field_1 == 6) {
            native_fn_ov000_021fbdec(1, 1, 0);
        } else {
            native_fn_ov000_021fbdec(1, 0, 0);
        }
        native_fn_0205f35c(-1, 0x9A);
        native_data_ov000_0223716c.field_1 = 3U;
        break;
    case 3:
        if (M2C_FIELD(temp_r0, u16 *, 2) & 0xFF7) {
            native_data_ov000_0223716c.field_1 = 4U;
        }
        break;
    case 4:
        native_fn_0204b380(temp_r4 + 0x10, 1);
        native_fn_ov000_02217c9c(1);
        native_fn_ov000_021fbcb8();
        var_r5 = 1;
        native_data_ov000_0223716c.field_1 = 0U;
        break;
    }
    return var_r5;
}
