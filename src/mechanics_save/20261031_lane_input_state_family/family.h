typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
#define FIELD(p,t,n) (*(t *)((u8 *)(p)+(n)))
__declspec(align(4)) extern u8 *native_data_021cfcb4;
