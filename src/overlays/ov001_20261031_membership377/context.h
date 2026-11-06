typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
#define FIELD(value,type,offset) (*(type)((u8 *)(value)+(offset)))
extern void *native_fn_02062a50(s32);
extern void *native_fn_02062a88(s32);
