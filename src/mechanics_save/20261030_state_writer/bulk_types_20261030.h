#ifndef PRIVATE_BULK_TYPES_20261030
#define PRIVATE_BULK_TYPES_20261030
typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct BulkRow {
    u32 uid;
    u8 unknown[2];
    u8 x;
    u8 y;
    u8 group;
    u8 enabled;
    u8 flagA;
    u8 flagB;
    s8 sprite;
    s8 marker;
    u8 tail[2];
} BulkRow;
typedef struct BulkSelection {
    s8 group;
    s8 previous;
    u8 x;
    u8 y;
    u8 dragging;
    s8 index;
    u8 pending;
} BulkSelection;
typedef struct BulkLayout {
    u8 field0;
    u8 x;
    u8 y;
    u8 width;
    u8 field4;
} BulkLayout;
typedef struct BulkEngine {
    u8 prefix;
    u8 groupCount;
    u8 unknown02[3];
    u8 destination;
    u8 special;
    u8 footerMode;
    u8 unknown08;
    s8 field09;
    u8 unknown0A[18];
    u8 savedX;
    u8 savedY;
    s8 savedIndex;
    s8 previousIndex;
    u8 unknown20[2];
    BulkLayout layouts[3];
} BulkEngine;
typedef struct BulkRecord {
    u8 prefix[24];
    s16 species;
} BulkRecord;
typedef struct BulkRuntime {
    u8 prefix[16];
    s8 kind;
} BulkRuntime;
#endif
