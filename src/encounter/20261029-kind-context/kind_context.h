#ifndef KIND_CONTEXT_20261029
#define KIND_CONTEXT_20261029
typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u16 word0;
    u16 word2;
    u8 byte4;
    u8 byte5;
    u8 byte6;
    u8 byte7;
    u32 unknown8[9];
} FieldRecord;
typedef struct { u32 unknown0[24]; u8 byte60; u8 byte61; u8 unknown62[2]; } KindRecord;
typedef struct { u32 magic; u32 count; KindRecord records[1]; } KindFile;
typedef struct { KindFile *file; KindRecord *records; } KindManager;
typedef char FieldRecordSize[sizeof(FieldRecord) == 44 ? 1 : -1];
typedef char KindRecordSize[sizeof(KindRecord) == 100 ? 1 : -1];
#endif
