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
extern u32 native_fn_02041538();
extern u32 native_fn_0205fa4c();
extern u32 native_fn_ov001_021fd354();
extern u32 native_fn_ov001_021fe2b8();
extern u32 native_fn_ov001_02202360();
extern u32 native_fn_ov001_02202d8c();
extern u32 native_fn_ov001_022043f0();
extern u32 native_fn_ov001_0220451c();
extern u32 native_fn_ov001_02204590();
extern u32 native_fn_ov001_02207f9c();
extern u32 native_fn_ov001_02208118();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x1];
    s8 field_c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_0220021c(void) {
    u8 temp_r1;
    s8 var_r2;
    u32 var_r4;
    u8 *temp_r5;
    u8 *temp_r6;

    var_r4 = 0;
    temp_r5 = native_fn_ov001_02202360(native_data_ov001_02239c10.field_c);
    temp_r6 = native_fn_ov001_02202360(0);
    if (native_fn_ov001_02207f9c() != 0) {
        native_fn_ov001_02208118();
        native_fn_ov001_02202d8c();
        native_fn_ov001_021fd354(0);
        native_fn_ov001_021fe2b8(1, 1);
        temp_r1 = M2C_FIELD(temp_r5, u8 *, 0x14);
        if (temp_r1 == 0) {
            var_r2 = M2C_FIELD(temp_r5, s8 *, 8);
        } else {
            var_r2 = M2C_FIELD(temp_r5, s8 *, 0xA);
        }
        native_fn_ov001_022043f0(temp_r5 + 0xA8, temp_r1, var_r2, 0x6B);
        native_fn_ov001_0220451c(temp_r6 + 0x18, *(u32 *)temp_r6);
        native_fn_ov001_02204590(temp_r6 + 0x18, 0x7D);
        if ((M2C_FIELD(temp_r5, u8 *, 0x14) == 1) && (native_data_ov001_02239c10.field_c == 1)) {
            native_fn_0205fa4c(temp_r5 + 0x60, 1);
        }
        var_r4 = 1;
        native_fn_02041538(0, 2, 0xA);
        native_data_ov001_02239c10.field_a = 7;
    }
    return var_r4;
}
