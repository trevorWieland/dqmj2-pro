typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0220dcb8 / 0x0220dd4c and 0x02004cd8: the two values handed to the display
   helper. Declared as the scalars they are; a pointer declaration costs a load. */
extern u32 native_data_0220dcb8;
extern u32 native_data_0220dd4c;
extern u32 native_data_02004cd8;

extern void native_fn_ov006_021f27d4(const void *first, const void *second);
