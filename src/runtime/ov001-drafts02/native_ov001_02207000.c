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
extern u32 native_fn_ov001_021fe6cc();
extern u32 native_fn_ov001_02204250();
extern u32 native_fn_ov001_022042c4();
extern u32 native_fn_ov001_022068a0();
void native_ov001_02207000(void) {
    u32 temp_r4;
    s8 var_r5;

    temp_r4 = native_fn_ov001_022068a0();
    var_r5 = 0;
    do {
        native_fn_02049ad0(var_r5);
        native_fn_ov001_021fe6cc();
        var_r5 += 1;
    } while ((s32) var_r5 <= 6);
    if (M2C_FIELD(temp_r4, s8 *, 0x91) == 0) {
        return;
    }
    native_fn_ov001_02204250(M2C_FIELD(temp_r4, s8 *, 0x92));
    native_fn_ov001_022042c4();
}
