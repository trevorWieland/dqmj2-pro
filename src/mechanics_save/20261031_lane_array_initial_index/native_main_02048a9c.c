typedef unsigned char u8;
typedef unsigned int u32;
u32 native_main_02048a9c(void *record,u32 value) {
    *((u8 *)record+0x79)=(u8)value;
    return (u32)record;
}
