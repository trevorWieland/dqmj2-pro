typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
#define M2C_FIELD(value,type,offset) (*(type)((s8 *)(value)+(offset)))
#define NULL ((void *)0)
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern s32 native_fn_0200a440(u32,u32,u32);
extern u8 native_data_020e53d0[];
