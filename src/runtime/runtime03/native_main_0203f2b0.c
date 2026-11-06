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
extern u32 native_fn_020273f0();
extern u32 native_fn_0205bf1c();
extern u32 native_fn_0205bf2c();
extern u32 native_fn_0205c314();
extern u32 native_fn_020725a0();
extern u32 native_fn_ov000_021df1f0();
extern u32 native_fn_ov000_021df3bc();
extern u32 native_fn_ov000_02214fc8();
extern u8 native_data_020f6054[];
u32 native_main_0203f2b0(void) {
    u32 var_r4;

    var_r4 = 1;
    if (M2C_FIELD(native_data_020f6054, s32 *, 0x30) == 0) {
        M2C_FIELD(native_data_020f6054, s8 *, 4) = (s8) native_fn_0205bf1c();
        native_fn_ov000_021df1f0();
        native_fn_020725a0((u32) (*(u16 *) native_fn_ov000_021df3bc() << 0x10) >> 0x1B);
        native_fn_0205c314(0);
        native_fn_0205bf2c(5);
        native_fn_ov000_02214fc8(2);
        M2C_FIELD(native_data_020f6054, s32 *, 0x30) = 0xA;
    }
    if ((M2C_FIELD(native_data_020f6054, s32 *, 0x30) == 0xA) && (native_fn_020273f0() == 0)) {
        M2C_FIELD(native_data_020f6054, s32 *, 0x30) = 0;
        var_r4 = 5;
    }
    return var_r4;
}
