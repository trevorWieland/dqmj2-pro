typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0221c148: scalar holding the base pointer; the row starts at +0x4c4. */
extern u32 native_data_ov006_0221c148;
extern u8 native_data_ov006_0220e1bc[];

extern void native_fn_0200616c(s32 arg, void *table, u32 a, u32 b, u32 c, u32 d);

/* Hand the caller's record row to the shared renderer. */
void native_ov006_021ff02c(s32 arg)
{
    u32 base = native_data_ov006_0221c148;
    u8 *row = (u8 *)(base + 0x4C4);

    native_fn_0200616c(arg, native_data_ov006_0220e1bc, row[0], row[1], row[2], row[3]);
}
