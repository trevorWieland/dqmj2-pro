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

typedef struct {
    u8 pad[0x34];
    u32 record;
} block_view;

/* Start the channel hand-off: read the record, derive the offset and dispatch. */
void native_ov006_021f4c80(s32 arg)
{
$DECLS
$READ_BLOCK
    $CHANNEL_ASSIGN
    $OFFSET_ASSIGN

    offset += $OFFSET_BIAS;
    native_fn_ov006_021f4944($MODE_ARG, offset);
    if (offset >= $THRESHOLD)
        native_fn_ov006_02204970(arg, (void (*)(void))$CALLBACK);
}
