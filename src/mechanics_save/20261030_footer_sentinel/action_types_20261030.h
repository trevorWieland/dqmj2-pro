#ifndef PRIVATE_ACTION_TYPES_20261030
#define PRIVATE_ACTION_TYPES_20261030
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Selection {
    s8 group;
    s8 previousGroup;
    u8 x;
    u8 y;
    u8 dragging;
    s8 dragIndex;
    u8 pending;
} Selection;
typedef struct Row {
    u32 uid;
    u8 unknown[2];
    u8 x;
    u8 y;
    u8 group;
    u8 enabled;
    u8 flagA;
    u8 flagB;
    s8 sprite;
    u8 tail[3];
} Row;
typedef struct Engine {
    u8 prefix;
    u8 count;
    u8 result;
    u8 unknown;
    u8 mode;
    u8 destination;
    u8 special;
    u8 footerIndex;
    u8 tail[2];
    u8 fieldA;
} Engine;
typedef struct Record {
    u8 prefix[0x18];
    s16 species;
    u8 form;
    u8 unknown[2];
    u8 field1D;
} Record;
typedef struct RuntimeInfo {
    u8 prefix[0x10];
    s8 kind;
} RuntimeInfo;
#endif
