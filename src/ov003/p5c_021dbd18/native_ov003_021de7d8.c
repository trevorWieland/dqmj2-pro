typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u8 native_data_ov003_021e03bc[];
extern u8 native_data_ov003_021e0b98[];

extern s32 native_fn_02065730(u8 *, s32, u32, u32, s32);

/* Fold nine scaled source records into the value array, indexed by each 3-byte
   entry's slot byte. */
void native_ov003_021de7d8(s32 *values) {
    s32 i = 0;
    u8 *entry = native_data_ov003_021e03bc;
    u8 *source = native_data_ov003_021e0b98;

    do {
        s32 index = entry[2];
        values[index] += native_fn_02065730(source, (s8)entry[0], entry[1], index, values[index]);
        entry += 3;
        source += 0xc;
        i++;
    } while (i < 9);
}
