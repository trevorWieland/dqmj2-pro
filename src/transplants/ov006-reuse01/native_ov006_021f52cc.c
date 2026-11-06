typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov006_0221c06c[];
void native_ov006_021f52cc(u32 value) {
    *(volatile u32 *)(native_data_ov006_0221c06c + 12) = value;
}
