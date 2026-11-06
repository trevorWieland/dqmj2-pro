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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fde70(void);
extern u32 native_arm7_fn_037fdca8(u32);
extern u32 native_arm7_fn_037fd7a8(u32);
extern u32 native_arm7_fn_037fdd14(u32);
extern u16 native_arm7_data_04000006;
u32 native_arm7_wram_037fd928(void *arg0, s16 arg1, s16 arg2, s32 arg3, s32 arg4) {
    u32 var_r0;
    u32 temp_r4;
    u16 temp_sb;

    temp_r4 = native_arm7_fn_037fdd00();
    if ((arg0 == NULL) || (M2C_FIELD(arg0, s32 *, 0) != 0)) {
        native_arm7_fn_037fde70();
    }
    temp_sb = native_arm7_data_04000006;
    var_r0 = native_arm7_fn_037fdca8((u32) temp_sb);
    M2C_FIELD(arg0, s32 *, 0x1C) = 1;
    M2C_FIELD(arg0, s16 *, 0x10) = arg1;
    if ((s32) arg1 <= (s32) temp_sb) {
        var_r0 += 1;
    }
    M2C_FIELD(arg0, u32 *, 0xC) = var_r0;
    M2C_FIELD(arg0, s16 *, 0x12) = arg2;
    M2C_FIELD(arg0, s32 *, 0) = arg3;
    M2C_FIELD(arg0, s32 *, 4) = arg4;
    M2C_FIELD(arg0, s32 *, 0x24) = 0;
    native_arm7_fn_037fd7a8((u32) arg0);
    return native_arm7_fn_037fdd14(temp_r4);
}
