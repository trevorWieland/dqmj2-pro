typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_arm7_data_03809edc[];
u32 native_arm7_wram_038052a8(void) {
    return *(volatile u32 *)(native_arm7_data_03809edc + 4);
}
