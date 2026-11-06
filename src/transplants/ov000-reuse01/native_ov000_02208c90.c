typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov000_02238510[];
void native_ov000_02208c90(u32 value) {
    *(volatile u8 *)(native_data_ov000_02238510 + 0) = value;
}
