#define NULL ((void *)0)
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
extern u32 native_fn_02049008();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0206006c();
extern u32 native_fn_0206b324();
extern u32 native_fn_020851d4();
extern u32 native_fn_ov001_0220a5c0();
extern u32 native_fn_ov001_0220aa54();
extern u8 native_data_ov001_0223df58[];
u32 native_ov001_0220b21c(u32 arg0) {
    u32 temp_r0_2;
    u8 *temp_r0;
    void *temp_r3;
    s8 var_r5;
    void *temp_r6;

    if (native_fn_ov001_0220a5c0() == 1) {
        native_fn_0206b324(0);
    } else {
        native_fn_02049008(arg0, 0xC, 0, 1, 4);
    }
    var_r5 = 0;
    do {
        temp_r0 = native_fn_02049ad0(var_r5);
        temp_r6 = M2C_FIELD(temp_r0, void **, 0);
        if ((temp_r6 != NULL) && ((M2C_FIELD(M2C_FIELD(temp_r6, void **, 4), s32 *, 0x18) & 2) == 2)) {
            temp_r0_2 = native_fn_ov001_0220aa54(M2C_FIELD(temp_r0, s8 *, 5));
            if ((temp_r0_2 != 0x7F) && (M2C_FIELD(temp_r0, s8 *, 5) != 0x7F)) {
                temp_r3 = M2C_FIELD(temp_r6, void **, 4);
                native_fn_0206006c((0xC * temp_r0_2) + (s32) native_data_ov001_0223df58, M2C_FIELD(temp_r3, s8 *, 0x5C), M2C_FIELD(temp_r3, s8 *, 0x5D), M2C_FIELD(temp_r3, s8 *, 0x5E), (s32) M2C_FIELD(temp_r3, s8 *, 0x5F));
            }
        }
        var_r5 += 1;
    } while ((s32) var_r5 < 0x24);
    return native_fn_020851d4();
}
