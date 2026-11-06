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
#define NULL ((void *)0)
extern u32 native_fn_0200708c();
extern u32 native_fn_02007110();
extern u32 native_fn_0203a5ec();
extern u32 native_fn_0203b854();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_020f4c84;
extern Record_native_data_020f4c84 native_data_020f4c84;
extern u8 native_data_020f5508[];
u32 native_main_0203a554(void *arg0) {
    native_fn_0200708c(native_data_020f5508);
    if (native_data_020f4c84.field_4 != 0) {
        native_fn_0200708c(native_data_020f4c84.field_4 + 0x4C8);
    }
    if (((s32) ((u32)M2C_FIELD(arg0, s32 *, 0x110) << 0x1E) >> 0x1F) != 0) {
        native_fn_0203b854(arg0);
    }
    if (((s32) ((u32)M2C_FIELD(arg0, s32 *, 0x110) << 0x1F) >> 0x1F) != 0) {
        M2C_FIELD(arg0, u32 (**)(void *), 0x170)(arg0);
    }
    native_fn_0203a5ec(arg0);
    native_fn_02007110((u32) native_data_020f5508);
    if (native_data_020f4c84.field_4 == 0) {
        return native_data_020f4c84.field_4;
    }
    return native_fn_02007110(native_data_020f4c84.field_4 + 0x4C8);
}
