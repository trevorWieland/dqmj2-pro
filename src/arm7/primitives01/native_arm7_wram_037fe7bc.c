typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_arm7_data_04000500[];
void native_arm7_wram_037fe7bc(u32 value) {
    *(volatile u8 *)(native_arm7_data_04000500 + 0) = value;
}
