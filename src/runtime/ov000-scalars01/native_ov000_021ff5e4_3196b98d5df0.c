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
extern u32 native_fn_ov000_02215698();
extern u32 native_fn_ov000_022156d4();
extern u32 native_fn_ov000_022162c0();
extern u32 native_fn_ov000_02216664();
extern u8 native_data_ov000_02237778[];
extern u8 native_data_ov000_02237870[];
extern u8 native_data_ov000_02237960[];
u32 native_ov000_021ff5e4(s32 arg0) {
    u32 temp_r4;

    temp_r4 = native_fn_ov000_02215698();
    switch (arg0) {
    case 1:
        native_fn_ov000_022156d4();
        break;
    case 3:
        native_fn_02049ad0(1);
        native_fn_ov000_022162c0();
        native_fn_0204b61c(temp_r4 + 0x10, 0);
        native_fn_ov000_02216664(native_data_ov000_02237870);
        *(u32 *)native_data_ov000_02237778 = 0;
        break;
    case 5:
        native_fn_02049ad0(2);
        native_fn_ov000_022162c0();
        native_fn_02049ad0(0x18);
        native_fn_ov000_022162c0();
        native_fn_02049ad0(0x19);
        native_fn_ov000_022162c0();
        native_fn_02049ad0(0x1B);
        native_fn_ov000_022162c0();
        native_fn_02049ad0(0x1C);
        native_fn_ov000_022162c0();
        native_fn_0204b61c(temp_r4 + 0x10, 0);
        native_fn_ov000_02216664(native_data_ov000_02237960);
        *(u32 *)native_data_ov000_02237778 = 2;
        break;
    }
    return *(u32 *)native_data_ov000_02237778;
}
