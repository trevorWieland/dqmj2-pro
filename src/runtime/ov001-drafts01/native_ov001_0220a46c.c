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
extern u32 native_fn_02041814();
extern u32 native_fn_0205fd0c();
extern u32 native_fn_0205fd34();
extern u32 native_fn_0205fd40();
extern u32 native_fn_0205fd60();
extern u32 native_fn_0205fd70();
extern u32 native_fn_02062378();
extern u32 native_fn_02071b9c();
extern u32 native_fn_0207f254();
extern u32 ov001_table_f0_entry_02202360();
extern u32 native_fn_ov001_0220a97c();
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0x3];
    u8 field_6;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
u32 native_ov001_0220a46c(void) {
    if (native_data_ov001_0223def8.field_2 == 0) {
        native_fn_02041538(1, 2, 0x1E);
        native_data_ov001_0223def8.field_2 = 0xA;
        goto block_6;
    }
    if ((native_data_ov001_0223def8.field_2 == 0xA) && (native_fn_02041814() != 1) && (native_fn_0205fd60() == 0)) {
        native_data_ov001_0223def8.field_2 = 0;
        return 7U;
    }
block_6:
    if (native_fn_0205fd70() != 0) {
        native_fn_0205fd34(native_fn_0205fd70(), 0x10);
        if (native_fn_0205fd70() != 0) {
            do {
                if (native_fn_02062378() != 6) {
                    native_fn_0205fd40();
                } else {
                    native_fn_02071b9c();
                    native_fn_0205fd70();
                    native_fn_0205fd0c();
                }
            } while (native_fn_0205fd70() != 0);
        }
    }
    if (native_data_ov001_0223def8.field_6 != 0) {
        ov001_table_f0_entry_02202360(6);
        native_fn_ov001_0220a97c();
    } else {
        native_fn_0207f254();
    }
    return 6U;
}
