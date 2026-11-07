#ifndef FIELD_METADATA_20261029
#define FIELD_METADATA_20261029
typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u16 word0;
    u16 word2;
    u8 byte4;
    u8 unknown5[15];
    u32 word14;
    u8 unknown18[20];
} FieldRecord;
typedef struct { u32 magic; u32 count; FieldRecord records[1]; } FieldFile;
typedef struct { FieldFile *file; FieldRecord *records; } FieldManager;
typedef struct { s16 id; u16 unknown2; FieldRecord record; } CacheSlot;
typedef struct { u16 id : 12; u16 kind : 4; } CompactField;
extern FieldManager native_data_021d5404;
extern CacheSlot native_data_021d540c[24];
extern CompactField native_data_021d588c[1421];
typedef char RecordSizeCheck[sizeof(FieldRecord) == 44 ? 1 : -1];
typedef char CacheSizeCheck[sizeof(CacheSlot) == 48 ? 1 : -1];
typedef char CompactSizeCheck[sizeof(CompactField) == 2 ? 1 : -1];
#endif
