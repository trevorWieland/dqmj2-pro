typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0221c060: block whose word at +0x34 points at the channel record. */
extern u32 *native_data_ov006_0221c060;

extern void native_fn_ov006_021f4944(s32 mode, s32 offset);
extern void native_fn_ov006_02204970(s32 arg, void (*callback)(void));

/* Start the channel hand-off: read the record, derive the offset and dispatch. */
void native_ov006_021f4c80(s32 arg)
{
    volatile s32 channel;
    s32 offset;
    u32 block = *native_data_ov006_0221c060;
    u32 record = *(u32 *)(block + 0x34);
    u32 value = *(u32 *)record;

    channel = (s32)((value & 0x01FF0000) >> 16);
    offset = (s32)(value & 0xFF);
    offset += 0xC;
    native_fn_ov006_021f4944(3, offset);
    if (offset >= 0xC0)
        native_fn_ov006_02204970(arg, (void (*)(void))0x021F4CC5);
}
