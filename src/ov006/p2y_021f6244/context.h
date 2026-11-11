typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0220df3c: display table handed to the helper. */
extern u32 native_data_0220df3c;
/* 0x0220df50: display table handed to the helper. */
extern u32 native_data_0220df50;
/* 0x0220df64: display table handed to the helper. */
extern u32 native_data_0220df64;
/* 0x02004cd8: accepted main ARM function (96 B) the helper reaches with blx r5.
   It is a function designator, not a data symbol. */
extern void native_fn_02004cd8();

/* 0x021f27d4: shared display helper. */
extern void native_fn_ov006_021f27d4(const void *table, void (*callback)(void));
