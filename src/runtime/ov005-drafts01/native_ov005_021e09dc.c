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
extern u32 native_fn_020414c8();
extern u32 native_fn_02041538();
extern u32 native_fn_02041908();
extern u32 native_fn_0204b61c();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0a74();
extern u32 native_fn_ov005_021e0a84();
typedef struct {
    u8 unknown_0[0x18];
    s32 field_18;
    u8 unknown_1c[0xc];
    u32 field_28;
} Record_native_data_ov005_021ed234;
extern Record_native_data_ov005_021ed234 native_data_ov005_021ed234;
u32 native_ov005_021e09dc(void) {
    if (native_data_ov005_021ed234.field_28 != 1) {
        return native_data_ov005_021ed234.field_28;
    }
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 0xFF7) {
        native_fn_ov005_021e0818();
        native_fn_0204b61c(native_fn_ov005_021e0a74(), 1);
        native_data_ov005_021ed234.field_28 = 0U;
        native_fn_02041538(0, 2, 8);
        native_fn_02041908(8, 0xA);
        native_fn_020414c8(0x3F);
        native_data_ov005_021ed234.field_18 = 0;
    }
    return 1U;
}
