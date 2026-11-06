typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_ov006_0221c0e8[];
void native_ov006_021fa158(u32 value) {
    *(volatile u32 *)(native_data_ov006_0221c0e8 + 0) = value;
}
