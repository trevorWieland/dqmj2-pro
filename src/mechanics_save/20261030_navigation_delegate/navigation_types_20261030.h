#ifndef PRIVATE_NAVIGATION_TYPES_20261030
#define PRIVATE_NAVIGATION_TYPES_20261030
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Input {
    u16 prefix;
    u16 pressed;
    u16 unknown;
    u16 repeated;
} Input;
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
    u8 prefix[7];
    u8 y;
    u8 unknown[4];
    s8 sprite;
    u8 tail[3];
} Row;
#endif
