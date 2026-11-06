typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct CopyStateView { u8 prefix[0x384]; u16 values[16]; } CopyStateView;
typedef struct WordStateView { u8 prefix[0x33a]; u16 control; u8 gap[0x2b4]; u16 multiplier,increment; volatile u16 state; } WordStateView;
extern u32 native_arm7_data_0380fff4;
extern u32 native_utility_child_arm7_data_0380fff4[];
#define NATIVE_HALFWORD_INPUT (*(volatile u16 *)0x0480802a)
#define NATIVE_HALFWORD_OUTPUT (*(volatile u16 *)0x04808028)
typedef char NativeHalfwordWidth[(sizeof(u16)==2)?1:-1];
typedef char NativeAddressWidth[(sizeof(void *)==4)?1:-1];
