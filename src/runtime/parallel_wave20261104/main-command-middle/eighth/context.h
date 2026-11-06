typedef unsigned int u32;
typedef struct ArgumentBlock { u32 output; u32 enabled; u32 include4; u32 input; } ArgumentBlock;
extern u32 native_fn_02048f7c(u32);
extern void native_fn_02049c90(u32, ArgumentBlock *, u32);
extern void native_fn_02049e28(u32, u32, u32);
extern void native_fn_020414c8(u32);
extern void native_fn_02041538(u32, u32, u32);
extern void native_fn_0204157c(u32);

typedef unsigned char u8;
typedef signed char s8;
typedef struct LinkView { s8 first; u8 gap1[3]; void *resource; } LinkView;
typedef struct EntryView { LinkView *link; s8 field4; s8 field5; s8 field6; u8 gap7; } EntryView;
extern LinkView *native_fn_0205fe20(int);
extern void native_fn_0205fe74(LinkView *, u32, u32, u32, u8, u8, u8, u8, u32, s8, u32);
extern u8 native_data_021029c8[];
extern u8 native_data_021029d0[];

typedef char ArgumentSize[(sizeof(ArgumentBlock) == 16) ? 1 : -1];
typedef char EnabledOffset[((u32)&((ArgumentBlock *)0)->enabled == 4) ? 1 : -1];
typedef char IncludeOffset[((u32)&((ArgumentBlock *)0)->include4 == 8) ? 1 : -1];
typedef char InputOffset[((u32)&((ArgumentBlock *)0)->input == 12) ? 1 : -1];
typedef char EntrySize[(sizeof(EntryView) == 8) ? 1 : -1];
typedef char EntryTagOffset[((u32)&((EntryView *)0)->field6 == 6) ? 1 : -1];
typedef char SignedByte[(sizeof(s8) == 1 && (s8)0x80 == -128 && (s8)255 == -1) ? 1 : -1];
typedef char UnsignedByte[(sizeof(u8) == 1 && (u8)-1 == 255) ? 1 : -1];
