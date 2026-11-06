typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov000_022381a8[];
u32 native_ov000_0220610c(void) {
    return *(volatile u32 *)(native_data_ov000_022381a8 + 4);
}
