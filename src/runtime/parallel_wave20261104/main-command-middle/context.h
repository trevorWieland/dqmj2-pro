typedef unsigned char u8;
typedef short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct MessageRecord { u8 reserved[0x3544]; u32 words[128]; } MessageRecord;
extern void native_fn_02047ff0(const u8 *, int, u32);
#define MESSAGE_RECORDS ((MessageRecord *)0x020fbae8)
