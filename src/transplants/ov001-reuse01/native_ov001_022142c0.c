typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov001_02242aac[];
u32 native_ov001_022142c0(void) {
    return *(volatile u32 *)(native_data_ov001_02242aac + 4);
}
