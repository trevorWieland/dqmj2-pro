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
extern u32 native_fn_ov001_021fc738();
extern u32 native_fn_ov001_021fd330();
extern u32 native_fn_ov001_021fd9a8();
extern u32 native_fn_ov001_021fda70();
extern u32 native_fn_ov001_021fdc8c();
extern u32 native_fn_ov001_021fe0a4();
extern u32 native_fn_ov001_021fe2b8();
extern u32 native_fn_ov001_021fe864();
extern u32 native_fn_ov001_021fec1c();
extern u32 native_fn_ov001_021fee8c();
extern u32 native_fn_ov001_022023dc();
extern u32 native_fn_ov001_022023f8();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov001_0222ed34;
extern Record_native_data_ov001_0222ed34 native_data_ov001_0222ed34;
typedef struct {
    u8 unknown_0[0xe];
    s8 field_e;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_02202120(void) {
    u32 temp_r0;

    if (native_fn_ov001_022023f8(2) != 0) {
        native_fn_ov001_021fd330();
        native_fn_ov001_021fe2b8(native_data_ov001_02239c10.field_e, 0);
        native_fn_ov001_021fec1c(native_data_ov001_0222ed34.field_4);
        native_fn_ov001_022023dc(2);
    }
    if (native_fn_ov001_022023f8(0x80) != 0) {
        native_fn_ov001_021fee8c();
        native_fn_ov001_022023dc(0x80);
    }
    if (native_fn_ov001_022023f8(1) != 0) {
        native_fn_ov001_021fc738();
        native_fn_ov001_022023dc(1);
    }
    if (native_fn_ov001_022023f8(4) != 0) {
        native_fn_ov001_021fda70();
        native_fn_ov001_021fdc8c();
        native_fn_ov001_021fd9a8();
        native_fn_ov001_022023dc(4);
    }
    if (native_fn_ov001_022023f8(8) != 0) {
        native_fn_ov001_021fe864();
        native_fn_ov001_022023dc(8);
    }
    temp_r0 = native_fn_ov001_022023f8(0x100);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_fn_ov001_021fe0a4();
    return native_fn_ov001_022023dc(0x100);
}
