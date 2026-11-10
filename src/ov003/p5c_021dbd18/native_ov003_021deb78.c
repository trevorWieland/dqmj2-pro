typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern void native_fn_ov003_021de868(s32, s32, s32, s32, s32, s32, s32, s32, s32);
extern void native_fn_ov003_021de9f0(s32, s32, s32, s32, s32);

/* Stage one record with the fixed nine-word descriptor, then route the caller's
   single operand through the secondary list. */
void native_ov003_021deb78(u8 *context, s32 arg1) {
    native_fn_ov003_021de868(0, (s8)context[0x10], 0x7f, 1, 1, 0x14, 2, 1, 1);
    native_fn_ov003_021de9f0(0, 0x14, 0, arg1, 8);
}
