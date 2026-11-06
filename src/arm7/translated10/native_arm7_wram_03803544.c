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
extern u32 native_arm7_fn_037fdef4(u32);
extern u32 native_arm7_fn_03806680(u32);
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fe708(void);
extern u32 native_arm7_fn_038052fc(void);
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_fn_037fde70(void);
u32 native_arm7_wram_03803544(u32 arg0, s32 arg1) {
    u32 temp_r4;

    if ((arg1 & 0x3F) == 1) {
        native_arm7_fn_037fdef4(0U);
        native_arm7_fn_037fdef4(1U);
        native_arm7_fn_037fdef4(2U);
        native_arm7_fn_037fdef4(3U);
        native_arm7_fn_03806680(0U);
        temp_r4 = native_arm7_fn_037fdd00();
        native_arm7_fn_037fe708();
        native_arm7_fn_038052fc();
        native_arm7_fn_037fdd14(temp_r4);
        return native_arm7_fn_037fde70();
    }
    return native_arm7_fn_037fde70();
}
