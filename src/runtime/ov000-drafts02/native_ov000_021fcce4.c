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
extern u32 native_fn_02049ad0();
extern u32 native_fn_ov000_022162c0();
extern u32 native_fn_ov000_02216664();
extern u32 native_fn_ov000_022167a8();
extern u32 native_fn_ov000_02217a54();
extern u32 native_fn_ov000_02217b64();
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
} Record_native_data_ov000_022372a8;
extern Record_native_data_ov000_022372a8 native_data_ov000_022372a8;
void native_ov000_021fcce4(s32 arg0) {
    switch (arg0) {
    case 2:
        native_fn_ov000_02216664(native_data_ov000_022372a8.field_c + 0xC);
        return;
    case 4:
        native_fn_ov000_02217b64();
        native_fn_ov000_02217a54();
        native_fn_ov000_02216664(native_data_ov000_022372a8.field_c + 0xFC);
        native_fn_ov000_022167a8(0x1B, 1, 2);
        native_fn_02049ad0(0x18);
        native_fn_ov000_022162c0();
        return;
    }
}
