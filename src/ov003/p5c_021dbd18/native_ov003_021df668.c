typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u32 native_fn_ov003_021dadb8(void);
extern void native_fn_02049b84(s32);
extern void native_fn_020414c8(u32);
extern void native_fn_ov003_021dfd18(s32);
extern u32 native_fn_02048f7c(s32);

/* Show the current slot with the given priority: refresh the slot table, apply
   the optional dim, then publish the entry through the selection hook. */
void native_ov003_021df668(s32 arg0) {
    u32 *context = (u32 *)native_fn_ov003_021dadb8();

    native_fn_02049b84(arg0);
    if (arg0 != 0) {
        native_fn_020414c8(0x3f);
    }
    native_fn_ov003_021dfd18(1);
    context[native_fn_02048f7c(1)] = 0x20;
}
