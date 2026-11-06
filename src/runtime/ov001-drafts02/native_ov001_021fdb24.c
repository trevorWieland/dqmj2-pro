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
extern u32 native_fn_0206d250();
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db530();
extern u32 native_fn_ov001_021fd074();
extern u32 native_fn_ov001_021fe934();
extern u32 native_fn_ov001_02202384();
extern u32 native_fn_ov001_02202398();
void native_ov001_021fdb24(void) {
    s32 temp_r0;
    s8 temp_r0_2;
    u32 temp_r4;
    u32 temp_r5;
    s32 temp_r9;
    s8 var_r10;
    s32 temp_gt;

    temp_r0 = (s32) native_fn_ov001_021db530(0);
    var_r10 = 0;
    if (temp_r0 <= 0) {
        return;
    }
    do {
        native_fn_ov001_021db438(0, var_r10);
        temp_r5 = native_fn_ov001_021fd074(0, var_r10);
        temp_r9 = (s32) (native_fn_ov001_02202384(0) << 0x15) >> 0x18;
        temp_r4 = native_fn_ov001_02202398(0, var_r10);
        native_fn_ov001_021fe934(8, (u8) temp_r9, (u8) (s8) ((native_fn_0206d250(M2C_FIELD(temp_r5, s8 *, 0xC)) * 5) + ((s32) temp_r4 >> 3) + 4));
        temp_r0_2 = var_r10 + 1;
        temp_gt = temp_r0 > (s32) temp_r0_2;
        var_r10 = temp_r0_2;
    } while (temp_gt);
}
