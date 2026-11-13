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
extern u32 native_fn_ov001_021fd858();
extern u32 native_fn_ov001_021fe3dc();
extern u32 ov001_table_f0_entry_02202360();
extern u32 native_fn_ov001_022023c4();
extern u32 native_fn_ov001_0220451c();
extern u32 native_fn_ov001_02204590();
extern u8 native_data_ov001_02239c10[];
u32 native_ov001_021ff238(void) {
    u32 temp_r4;

    temp_r4 = ov001_table_f0_entry_02202360(M2C_FIELD(native_data_ov001_02239c10, s8 *, 0xC));
    M2C_FIELD(native_data_ov001_02239c10, u8 *, 0) = 1;
    native_fn_ov001_022023c4(0x8F);
    native_fn_ov001_021fe3dc(1, 0);
    native_fn_ov001_021fd858();
    if (M2C_FIELD(temp_r4, s32 *, 0x34) != 0) {
        native_fn_ov001_02204590(temp_r4 + 0x18, 0x7D);
        native_fn_ov001_0220451c(temp_r4 + 0x18, M2C_FIELD(temp_r4, s32 *, 0));
    }
    M2C_FIELD(native_data_ov001_02239c10, s8 *, 0xA) = 0xB;
    return (u32) native_data_ov001_02239c10;
}
