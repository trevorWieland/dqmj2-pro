typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0220de60: display table handed to the helper. */
extern u32 native_data_0220de60;
/* 0x02004cd8: accepted main ARM function (96 B), passed as a designator. */
extern void native_fn_02004cd8();
extern void native_fn_ov006_021f27d4(const void *table, void (*callback)(void));

/* Display family, 80-byte body. */
void native_ov006_021f9d34(void)
{
    native_fn_ov006_021f27d4(&native_data_$TABLE, native_fn_02004cd8);
    *(u16 *)0x04001008 = (*(u16 *)0x04001008 & ~3) | 3;
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 3;
    *(u16 *)0x04000008 = (*(u16 *)0x04000008 & ~3) | 3;
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & ~3) | 3;
    *(u16 *)0x0400000C = (*(u16 *)0x0400000C & ~3) | 3;
}
