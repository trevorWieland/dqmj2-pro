typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov000_02246574[];
void native_ov000_02223318(u32 value) {
    *(volatile u8 *)(native_data_ov000_02246574 + 0) = value;
}
