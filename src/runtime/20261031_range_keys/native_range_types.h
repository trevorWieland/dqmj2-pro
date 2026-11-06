#ifndef NATIVE_RANGE_TYPES_H
#define NATIVE_RANGE_TYPES_H
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Node {
    u16 first;
    u16 last;
    u16 format;
    u16 reserved;
    const struct Node *next;
    u16 words[];
} Node;
typedef struct {
    u32 opaque[4];
    const Node *head;
} Map;
#endif
