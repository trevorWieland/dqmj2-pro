typedef unsigned char u8;
typedef short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct MessageRecord { u8 reserved[0x3544]; u32 words[128]; } MessageRecord;
extern void native_fn_02047ff0(const u8 *, int, u32);
#define MESSAGE_RECORDS ((MessageRecord *)0x020fbae8)
typedef struct TextCursor { u8 reserved[0x80]; u16 field80; } TextCursor;
extern u8 native_fn_02047ac0(u32);
extern u8 native_fn_02047b90(u16 *, u32, u32, u32);
extern u8 native_fn_02047bfc(u16 *, u32, u32, u32);
extern TextCursor native_data_020fb264;
extern u16 native_data_020fae64[];

typedef char CursorFieldOffset[((u32)&((TextCursor *)0)->field80 == 0x80) ? 1 : -1];
typedef char CursorPrefixSize[(sizeof(TextCursor) == 0x82) ? 1 : -1];
typedef char HalfwordWidth[(sizeof(u16) == 2) ? 1 : -1];
typedef char WordWidth[(sizeof(u32) == 4) ? 1 : -1];
