typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u8 native_data_ov003_021e03d7[];
extern u8 native_data_ov003_021e0a9c[];

extern s32 native_fn_02048f5c(s32);
extern s32 native_fn_0205ffcc(u8 *, s32, u32, u32, s32);

/* Fold twenty-one scaled source records into the entry selected by the shared
   slot helper, indexed by each 3-byte record's slot byte. */
void native_ov003_021de768(s32 *values) {
    s32 i;
    u8 *entry;
    u8 *source;
    s32 index;

    index = native_fn_02048f5c(1);
    entry = native_data_ov003_021e03d7;
    source = native_data_ov003_021e0a9c;
    i = 0;
    do {
        values[index] += native_fn_0205ffcc(source, (s8)entry[0], entry[1], index, values[index]);
        entry += 3;
        source += 0xc;
        i++;
    } while (i < 0x15);
}
