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
