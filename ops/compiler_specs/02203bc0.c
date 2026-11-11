typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

/* 0x0221c188: slot holding the stream callback. */
extern u32 *native_data_ov006_0221c188;

extern void native_fn_0202b328(u32 stream);

/* Release the stream and clear the slot. */
void native_ov006_02203bc0(void)
{
    native_fn_0202b328(*native_data_ov006_0221c188);
    *native_data_ov006_0221c188 = 0;
}
