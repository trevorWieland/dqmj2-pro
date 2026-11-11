/* Shared declarations for the ov001 accessor packet (ov001-u1).
 *
 * Overlay globals are declared as flat byte arrays and addressed with their
 * measured field offsets. Every symbol name carries its measured address, so the
 * comparison harness resolves relocations without any side table.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef long long s64;

/* 0x02238d40: per-entry selector records, 4 bytes apart. 0x02238d41 is the
   count byte inside the same records. */
extern u8 native_data_02238d40[];
extern u8 native_data_02238d41[];
/* 0x02238d1c / 0x02238d2e: two halfword tables with a 6-byte entry stride. */
extern u8 native_data_02238d1c[];
extern u8 native_data_02238d2e[];
/* 0x02238d1e / 0x02238d1f / 0x02238d30 / 0x02238d31: flag bytes inside the
   6-byte entries addressed through the two table bases. */
extern u8 native_data_02238d1e[];
extern u8 native_data_02238d1f[];
extern u8 native_data_02238d30[];
extern u8 native_data_02238d31[];
/* 0x02238e58 / 0x02238e5c: 32-entry registration table, 8 bytes per entry. */
extern u8 native_data_02238e58[];
extern u8 native_data_02238e5c[];

extern u8 *native_fn_0207afec();
extern u8 *native_fn_0205d750();
extern u32 native_fn_0205c79c(s32 key);
extern void native_fn_ov001_021ee564(s32 a, s32 b, s32 c, s32 d, s32 e, s32 f);
