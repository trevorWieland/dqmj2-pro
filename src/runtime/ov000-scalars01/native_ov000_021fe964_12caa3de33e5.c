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
extern u32 native_fn_0204b61c();
extern u32 native_fn_02061260();
extern u32 native_fn_020642dc();
extern u32 ov000_display_context_02215698();
extern u32 native_fn_ov000_022156d4();
extern u32 native_fn_ov000_022162c0();
extern u32 native_fn_ov000_02216664();
extern u8 native_data_ov000_02237564[];
extern u8 native_data_ov000_0223765c[];
u32 native_ov000_021fe964(s32 arg0) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = ov000_display_context_02215698();
    switch (arg0) {
    case 1:
        native_fn_ov000_022156d4();
        temp_r0 = native_fn_020642dc() - 0xE;
        switch (temp_r0) {
        default:
            break;
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
            native_fn_02061260(1);
            break;
        }
        break;
    case 3:
        native_fn_02049ad0(1);
        native_fn_ov000_022162c0();
        native_fn_0204b61c(temp_r4 + 0x10, 0);
        native_fn_ov000_02216664(native_data_ov000_0223765c);
        *(u32 *)native_data_ov000_02237564 = 0;
        break;
    }
    return *(u32 *)native_data_ov000_02237564;
}
