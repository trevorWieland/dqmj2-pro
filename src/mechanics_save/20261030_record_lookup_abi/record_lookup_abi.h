typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { u8 prefix[0x14]; u32 id; u8 remaining[0x6c]; } SavedRecord;
extern SavedRecord *native_fn_02062a10(u32 id);
