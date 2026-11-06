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
extern u32 native_fn_02049ae4();
extern u32 native_fn_02068f60();
extern u32 native_fn_02086b14();
extern u32 native_fn_ov001_021fd82c();
extern u32 native_fn_ov001_021fe3d0();
extern u32 native_fn_ov001_021fea80();
extern u32 native_fn_ov001_02203070();
extern u32 native_fn_ov001_02203308();
extern u32 native_fn_ov001_02203ccc();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
} Record_native_data_ov001_0223d8ec;
extern Record_native_data_ov001_0223d8ec native_data_ov001_0223d8ec;
u32 native_ov001_02203d74(void) {
    u32 temp_r4;
    void *temp_r2;

    temp_r4 = native_fn_02049ae4();
    native_fn_ov001_021fd82c();
    native_fn_ov001_021fe3d0(1, 1, 0xC);
    temp_r2 = M2C_FIELD(temp_r4, void **, 4);
    M2C_FIELD(temp_r2, s32 *, 0x18) = (s32) (M2C_FIELD(temp_r2, s32 *, 0x18) | 2);
    native_fn_02086b14(M2C_FIELD(temp_r4, void **, 4), 0xA);
    native_fn_ov001_021fea80();
    native_fn_02068f60(0);
    native_fn_ov001_02203308(0, 1);
    native_fn_ov001_02203ccc(0);
    native_fn_ov001_02203070();
    native_data_ov001_0223d8ec.field_8 = 7;
    return 0U;
}
