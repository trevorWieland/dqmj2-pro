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
extern u32 native_arm7_fn_03806680(u32);
extern u32 native_arm7_fn_037fe708(void);
extern u32 native_arm7_fn_038052fc(void);
extern u32 native_arm7_fn_037fde70(void);
u32 native_arm7_wram_0380663c(u32 arg0, s32 arg1) {
    if ((arg1 & 0x3F) == 2) {
        native_arm7_fn_03806680(0U);
        native_arm7_fn_037fe708();
        native_arm7_fn_038052fc();
        return native_arm7_fn_037fde70();
    }
    return native_arm7_fn_037fde70();
}
