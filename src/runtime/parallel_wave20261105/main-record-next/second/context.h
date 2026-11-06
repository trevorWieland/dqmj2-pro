typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u8 prefix[0x14];
    u32 id;
    u8 remaining[0x6c];
} SavedRecord;
typedef struct NativeInput {
    u8 reserved0000[0x10];
    s8 field0010;
} NativeInput;
typedef struct NativeRecord {
    u8 reserved0000[0x14];
    s32 field0014;
    s16 field0018;
} NativeRecord;
extern u32 native_fn_020c8fa8(void);
extern SavedRecord* native_fn_02062a10(u32);
extern SavedRecord* native_fn_02062a50(int);
extern u32 native_fn_02062aa0(void);
extern u32 native_fn_020629e0(void);
extern u32 native_fn_02072f48(s32);
extern u32 native_fn_020c9984(u32,u32,u32,s32,u8,u8,u8,s8,s32);
extern u32 native_fn_020ccd44(u32,u32,u32,s32,u8,u8,u8,s8,s32);
extern u32 native_fn_020c9a3c(s32,u32,u32,u32,s16);
extern u32 native_fn_020cce5c(s32,u32,u32,u32,s16);
extern u32 native_fn_020c9c10(u32,u32);
extern u32 native_fn_020c9a84(void*,s16,s16,s8,s8,s8,s32);
