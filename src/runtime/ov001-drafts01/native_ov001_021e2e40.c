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
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d774c();
extern u32 native_fn_ov001_021db410();
extern u32 ov001_side_slot_record_021db438();
extern u32 native_fn_ov001_021e34f0();
extern u32 native_fn_ov001_02218010();
extern u32 native_fn_ov001_0221806c();
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
    s8 field_3;
} Record_native_data_ov001_02238ad0;
extern Record_native_data_ov001_02238ad0 native_data_ov001_02238ad0;
u32 native_ov001_021e2e40(void) {
    s32 var_r8;

    if (native_data_ov001_02238ad0.field_2 == 0) {
        native_fn_ov001_021d75d4(0);
        native_fn_ov001_021e34f0(1);
        if (native_fn_ov001_0221806c() != 0) {
            native_fn_ov001_02218010(0);
        }
        var_r8 = 0;
        do {
            native_fn_ov001_021db410(ov001_side_slot_record_021db438(0, var_r8), 1);
            native_fn_ov001_021db410(ov001_side_slot_record_021db438(1, var_r8), 0);
            var_r8 += 1;
        } while (var_r8 < 3);
        native_data_ov001_02238ad0.field_2 = 0xAU;
    }
    if ((native_data_ov001_02238ad0.field_2 == 0xA) && (native_fn_ov001_021d774c(-1) == 0)) {
        native_data_ov001_02238ad0.field_2 = 0x64U;
    }
    if (native_data_ov001_02238ad0.field_2 == 0x64) {
        native_data_ov001_02238ad0.field_3 = 2;
        native_data_ov001_02238ad0.field_2 = 0U;
    }
    return 0U;
}
