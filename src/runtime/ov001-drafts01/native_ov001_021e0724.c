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
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d774c();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021e7fa8();
extern u32 native_fn_ov001_021f1294();
extern u32 native_fn_ov001_021f1324();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f949c();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x14];
    s8 field_1d;
    u8 unknown_1e[0x7];
    u8 field_25;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021e0724(void) {
    if (native_data_ov001_022388ec.field_25 == 0) {
        native_fn_ov001_021f1294(0x10, 2);
        native_fn_ov001_021f1354(1, 0, 5, 1);
        native_fn_ov001_021d75d4(0x2B);
        native_fn_ov001_021d94cc(0, 1);
        native_fn_ov001_021f949c(0xDE, 1);
        native_data_ov001_022388ec.field_25 = 0xAU;
    }
    if ((native_data_ov001_022388ec.field_25 == 0xA) && (native_fn_ov001_021d774c(-1) == 0)) {
        native_data_ov001_022388ec.field_25 = 0x64U;
    }
    if (native_data_ov001_022388ec.field_25 == 0x64) {
        native_fn_ov001_021f14a4();
        native_fn_ov001_021f1324();
        native_fn_ov001_021e7fa8();
        native_data_ov001_022388ec.field_1d = 1;
        native_data_ov001_022388ec.field_8 = 3;
        native_data_ov001_022388ec.field_25 = 0U;
    }
    return 0U;
}
