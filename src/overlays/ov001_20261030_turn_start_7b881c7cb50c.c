typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
extern void native_fn_02008d78(void *, u32, u32);
extern u32 native_fn_0203d2ec(u32);
extern u32 native_fn_02044508(void);
extern u32 native_fn_0204457c(void);
extern u32 ov001_mode_byte_021db530(signed int);
extern void native_fn_ov001_021dcabc(void);
extern void native_fn_ov001_021dcbe4(void);
extern u32 native_fn_ov001_021de590(void);
extern u32 native_fn_ov001_021e82ac(void);
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x2];
    s8 field_b;
    u8 unknown_c[0x2];
    s8 field_e;
    u8 unknown_f[0x3];
    s8 field_12;
    u8 unknown_13[0x7];
    s8 field_1a;
    u8 unknown_1b[0x3];
    s8 field_1e;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
extern u8 native_data_ov001_02238950[];
extern u8 native_data_ov001_0223896c[];
u32 native_ov001_021de598(void) {
    u32 temp_r4;

    temp_r4 = ov001_mode_byte_021db530(0);
    native_data_ov001_022388ec.field_e = (s8) (temp_r4 + ov001_mode_byte_021db530(1));
    native_data_ov001_022388ec.field_12 = 0;
    native_data_ov001_022388ec.field_1a = 0;
    native_data_ov001_022388ec.field_b = 0;
    if (native_fn_02044508() != 0) {
        native_fn_0203d2ec(native_fn_0204457c());
    }
    native_fn_ov001_021dcabc();
    native_fn_ov001_021dcbe4();
    native_data_ov001_022388ec.field_1e = (s8) native_fn_ov001_021e82ac();
    native_fn_02008d78(native_data_ov001_0223896c, 0, 0x1C);
    native_fn_02008d78(native_data_ov001_02238950, 0, 0x1C);
    if (native_fn_ov001_021de590() != 0) {
        native_data_ov001_022388ec.field_8 = 0x1F;
    } else {
        native_data_ov001_022388ec.field_8 = 0x21;
    }
    return 1U;
}
