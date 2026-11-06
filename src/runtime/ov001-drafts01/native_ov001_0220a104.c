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
extern u32 native_fn_02041814();
extern u32 native_fn_02068d54();
extern u32 native_fn_02069010();
extern u32 native_fn_020693e0();
extern u32 native_fn_0207e874();
extern u32 native_fn_0207e948();
extern u32 native_fn_ov001_021fd330();
extern u32 native_fn_ov001_021fd354();
extern u32 native_fn_ov001_0220b2fc();
typedef struct {
    u8 unknown_0[0x14];
    s32 field_14;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
u32 native_ov001_0220a104(void) {
    u32 var_r4;

    var_r4 = 0;
    switch (native_data_ov001_0223def8.field_14) {
    case 0:
        if (native_fn_02041814() == 1) {
            native_fn_0207e874();
            var_r4 = 2;
        } else {
            native_fn_0207e948();
            native_data_ov001_0223def8.field_14 = 1;
        }
        break;
    case 1:
        if (native_fn_02041814() == 1) {
            var_r4 = 2;
        } else {
            native_fn_ov001_0220b2fc();
            native_fn_02068d54();
            native_fn_020693e0();
            native_fn_02069010(0);
            native_fn_02069010(1);
            native_fn_02069010(2);
            native_fn_ov001_021fd354(0);
            native_data_ov001_0223def8.field_14 = 3;
        }
        break;
    case 3:
        native_fn_ov001_0220b2fc();
        native_fn_ov001_021fd330();
        native_data_ov001_0223def8.field_14 = 1;
        break;
    }
    return var_r4;
}
