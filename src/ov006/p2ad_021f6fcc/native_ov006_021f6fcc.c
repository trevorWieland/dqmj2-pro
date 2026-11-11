typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u8 native_data_ov006_0221c0b8;
extern s32 native_fn_ov006_021f2390(void);
extern void native_fn_ov006_021ff6d4(s32 mode);
extern void native_fn_ov006_021f52cc(void (*callback)(void));

/* Dispatch on the helper's result, then hand the follow-up callback over. */
void native_ov006_021f6fcc(void)
{
    switch (native_fn_ov006_021f2390()) {
    case 0:
        native_fn_ov006_021ff6d4(7);
        break;
    case 1:
        native_fn_ov006_021ff6d4(6);
        native_data_ov006_0221c0b8 = 1;
        break;
    default:
        return;
    }
    native_fn_ov006_021f52cc((void (*)(void))0x021F7001);
}
