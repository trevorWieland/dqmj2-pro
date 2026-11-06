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
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021dcff4();
extern u32 native_fn_ov001_021e29e8();
extern u32 native_fn_ov001_021e2a48();
extern u32 native_fn_ov001_021e8178();
extern u32 native_fn_ov001_021e871c();
extern u32 native_fn_ov001_022136b4();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x1];
    s8 field_a;
    u8 unknown_b[0x7];
    s8 field_12;
    u8 unknown_13[0x7];
    s8 field_1a;
    u8 unknown_1b[0x3];
    s8 field_1e;
    u8 unknown_1f[0x17];
    u16 field_36;
    u8 unknown_38[0x10];
    s32 field_48;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021df8d0(void) {
    s8 sp1;
    s8 sp0;

    native_data_ov001_022388ec.field_1a = (s8) (native_data_ov001_022388ec.field_1a + 1);
    if (((s32) native_data_ov001_022388ec.field_1a >= (s32) native_data_ov001_022388ec.field_a) || (M2C_FIELD((void *) native_fn_0207afec(native_data_ov001_022388ec.field_36), s8 *, 0x26) == 1)) {
        native_data_ov001_022388ec.field_1a = 0;
        native_data_ov001_022388ec.field_12 = (s8) (native_data_ov001_022388ec.field_12 + 1);
    } else {
        native_fn_ov001_021e8178(native_data_ov001_022388ec.field_12, &sp1, &sp0);
        native_fn_ov001_021e871c(sp1, sp0);
    }
    if (((s32) native_data_ov001_022388ec.field_12 >= (s32) native_data_ov001_022388ec.field_1e) || (native_fn_ov001_021e29e8() & 2)) {
        native_fn_ov001_021e2a48(2);
        native_data_ov001_022388ec.field_8 = 0x19;
    } else {
        native_data_ov001_022388ec.field_8 = 4;
    }
    native_fn_ov001_021dcff4(native_data_ov001_022388ec.field_48);
    native_fn_ov001_022136b4(0);
    return 1U;
}
