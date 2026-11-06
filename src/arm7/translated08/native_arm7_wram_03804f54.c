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
extern u32 native_arm7_fn_03804d14(u32);
extern u32 native_arm7_fn_03804cf0(u32);
extern u32 native_arm7_fn_037fde70(void);
extern u32 native_arm7_data_038075dc;
u32 native_arm7_wram_03804f54(u32 arg0) {
    switch (arg0) {
    case 1:
        native_arm7_fn_03804d14(0x10U);
        break;
    case 3:
        native_arm7_fn_03804cf0(0x30U);
        break;
    case 2:
        native_arm7_fn_03804d14(0x20U);
        native_arm7_fn_03804cf0(0x10U);
        break;
    default:
        native_arm7_fn_037fde70();
        break;
    }
    native_arm7_data_038075dc = arg0;
    return (u32) &native_arm7_data_038075dc;
}
