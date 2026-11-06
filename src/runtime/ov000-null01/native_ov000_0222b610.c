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
extern u32 native_fn_02045dc4();
extern u32 native_fn_02049008();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0206006c();
extern u32 native_fn_0206db90();
extern u32 native_fn_020851d4();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    s8 field_2;
    s8 field_3;
} Record_native_data_ov000_02247704;
extern Record_native_data_ov000_02247704 native_data_ov000_02247704;
extern u8 native_data_ov000_02247748[];
u32 native_ov000_0222b610(u32 arg0) {
    u32 temp_r0_2;
    u8 *temp_r0;
    void *temp_r3;
    s8 var_r7;
    void *temp_r8;

    native_fn_02049008(arg0, native_data_ov000_02247704.field_1, native_data_ov000_02247704.field_3, native_data_ov000_02247704.field_2, 2);
    var_r7 = 0;
    do {
        temp_r0 = native_fn_02049ad0(var_r7);
        temp_r8 = M2C_FIELD(temp_r0, void **, 0);
        if ((temp_r8 != NULL) && ((M2C_FIELD(M2C_FIELD(temp_r8, void **, 4), s32 *, 0x18) & 2) == 2)) {
            temp_r0_2 = native_fn_0206db90(M2C_FIELD(temp_r0, s8 *, 5));
            if (temp_r0_2 != 0x7F) {
                temp_r3 = M2C_FIELD(temp_r8, void **, 4);
                if (M2C_FIELD(temp_r0, s8 *, 5) == 0x7F) {
                    native_fn_02045dc4(1, 1, M2C_FIELD(temp_r3, u8 *, 0x5C), M2C_FIELD(temp_r3, u8 *, 0x5D), (s32) M2C_FIELD(temp_r3, u8 *, 0x5E), (s32) M2C_FIELD(temp_r3, u8 *, 0x5F));
                } else {
                    native_fn_0206006c((0xC * temp_r0_2) + (s32) native_data_ov000_02247748, (s8) M2C_FIELD(temp_r3, u8 *, 0x5C), (s8) M2C_FIELD(temp_r3, u8 *, 0x5D), (s8) M2C_FIELD(temp_r3, u8 *, 0x5E), (s32) (s8) M2C_FIELD(temp_r3, u8 *, 0x5F));
                }
            }
        }
        var_r7 += 1;
    } while ((s32) var_r7 < 0x24);
    return native_fn_020851d4();
}
