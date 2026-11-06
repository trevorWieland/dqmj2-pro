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
extern u32 native_fn_02040434();
extern u32 native_fn_0205d53c();
extern u32 native_fn_ov000_021d8958();
extern u32 native_fn_ov000_021d8ccc();
extern u32 native_fn_ov000_021da16c();
extern u32 native_fn_ov000_021e0764();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e52c0();
extern u32 native_fn_ov000_02211960();
extern u32 native_fn_ov000_0221310c();
extern u32 native_fn_ov000_02219e04();
extern u8 native_data_020f6054[];
u32 native_main_0203efa0(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_ov000_021e52c0() != 0) {
        var_r4 = 1;
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = (s8) M2C_FIELD(native_data_020f6054, s8 *, 0x11);
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 1) {
        native_fn_ov000_021e1894(0);
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 2) {
        native_fn_ov000_02219e04();
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 4) {
        native_fn_ov000_021d8ccc(-1, -1, -0x1000);
        native_fn_ov000_021d8958();
    }
    if ((M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 0x10) || (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 0x20)) {
        native_fn_ov000_021e0764();
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 8) {
        native_fn_0205d53c();
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 0x40) {
        native_fn_ov000_0221310c();
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 0x80) {
        native_fn_ov000_02211960(0);
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) & 0x100) {
        native_fn_ov000_021da16c();
    }
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x34) != 0) {
        native_fn_02040434();
    }
    return var_r4;
}
