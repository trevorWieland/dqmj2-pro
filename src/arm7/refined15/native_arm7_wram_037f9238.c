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
extern u32 native_arm7_fn_037fd5c0(u32);
extern u32 native_arm7_fn_027e9d00(void);
extern u32 native_arm7_fn_037f9198(void);
extern u32 native_arm7_fn_027e9d88(void);
extern u32 native_arm7_fn_027e9eec(void);
extern u32 native_arm7_fn_027ea9c8(u32, u32);
extern u32 native_arm7_fn_027eaa78(void);
extern u32 native_arm7_data_0380fff4;
extern u16 native_arm7_data_04808040;
void native_arm7_wram_037f9238(u16 arg0) {
    u16 temp_r0;
    void *temp_r4;

    temp_r4 = native_arm7_data_0380fff4 + 0x344;
    temp_r0 = M2C_FIELD(temp_r4, u16 *, 8);
    if (temp_r0 != arg0) {
        if (temp_r0 == 0x40) {
            native_arm7_fn_037fd5c0(native_arm7_data_0380fff4 + 0x634);
        }
        switch (arg0) {
        case 0x0:
            native_arm7_fn_027e9d00();
            break;
        case 0x10:
            native_arm7_data_04808040 = 0;
            native_arm7_fn_037f9198();
            native_arm7_fn_027e9d88();
            break;
        case 0x40:
            if (M2C_FIELD(temp_r4, u16 *, 0xC) == 2) {
                native_arm7_fn_027e9eec();
            }
            native_arm7_fn_027ea9c8(0x64U, (u32) native_arm7_fn_027eaa78);
            break;
        }
        M2C_FIELD(temp_r4, u16 *, 8) = arg0;
    }
}
