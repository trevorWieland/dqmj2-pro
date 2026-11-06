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
extern u32 native_arm7_fn_027f17d4(u32);
extern u32 native_arm7_fn_037f8598(u32, u32);
extern u32 native_arm7_fn_027f1088(u32);
extern u32 native_arm7_fn_027eaaf8(u32, u32);
extern u32 native_arm7_fn_027f0c7c(u32);
extern u32 native_arm7_fn_027f0ffc(u32, u32);
extern u32 native_arm7_fn_027edb20(void);
extern u32 native_arm7_data_0380fff4;
extern u32 native_arm7_data_027ed828;
u32 native_arm7_main_027ed770(void) {
    u16 temp_r1;
    u32 temp_r0;
    void *temp_r4;

    temp_r1 = M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x404);
    temp_r4 = native_arm7_data_0380fff4 + 0x404;
    switch (temp_r1) {
    case 0x60:
        temp_r0 = native_arm7_fn_027f17d4(M2C_FIELD(temp_r4, void **, 0x18) + 0x10);
        if (temp_r0 == 0) {
            M2C_FIELD(M2C_FIELD(temp_r4, void **, 0x1C), s16 *, 4) = 8;
            M2C_FIELD(temp_r4, s16 *, 0) = 0x63;
            return native_arm7_fn_037f8598(2U, 4U);
        }
        M2C_FIELD(temp_r4, s16 *, 0) = 0x61;
        native_arm7_fn_027f1088(temp_r0);
        return native_arm7_fn_027eaaf8((u32) M2C_FIELD(M2C_FIELD(temp_r4, void **, 0x18), u16 *, 0x18), (u32) &native_arm7_data_027ed828);
    case 0x63:
        native_arm7_fn_027f0c7c(1U);
        native_arm7_fn_027f0ffc(1U, 0U);
        M2C_FIELD(temp_r4, s16 *, 0) = 0;
        return native_arm7_fn_027edb20();
    default:
        return native_arm7_data_0380fff4 + 4;
    }
}
