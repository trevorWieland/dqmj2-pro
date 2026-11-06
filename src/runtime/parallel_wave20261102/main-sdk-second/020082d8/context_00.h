typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
void native_main_020082d8(u16 bank, u16 lockId);
typedef u32 OSIntrMode;
extern OSIntrMode native_fn_02007ff4(void);
extern OSIntrMode native_fn_02008008(OSIntrMode state);
typedef struct {
u32 field_0000;
u16 field_0004[9 ];
} NativeStorage_020e3728;
extern NativeStorage_020e3728 native_data_main_020e3728;
u32 native_fn_0200829c (u32 bitmap);
