typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0220dcb8 / 0x0220dd4c: data table handed to the display helper. */
extern u32 native_data_0220dcb8;
extern u32 native_data_0220dd4c;
/* 0x02004cd8: an accepted MAIN ARM FUNCTION (96 B), reached by the helper as
   `blx r5`. It is a function designator, not a data symbol -- the bytes are
   identical either way, but labeling it as data would poison source-linking and
   every future caller. */
extern void native_fn_02004cd8();

extern void native_fn_ov006_021f27d4(const void *first, const void *second);
