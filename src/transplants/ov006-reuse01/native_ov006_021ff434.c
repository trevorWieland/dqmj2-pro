typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov006_0221c148[];
u32 native_ov006_021ff434(void) {
    return *(volatile u32 *)(native_data_ov006_0221c148 + 0);
}
