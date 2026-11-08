#ifndef OAM_GETTER32_SOURCE1_H
#define OAM_GETTER32_SOURCE1_H

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u32 attr01;
    u16 attr2;
    u16 remaining;
} OamEntryView;

typedef struct {
    u8 unconsumed[8];
    OamEntryView *entries;
} OamDescriptorView;

typedef char OamEntryWidth[(sizeof(OamEntryView) == 8) ? 1 : -1];
typedef char OamWordWidth[(sizeof(u32) == 4) ? 1 : -1];

u32 native_ov006_02202f98(u32 descriptorWord, s32 index, u32 outXWord, u32 outYWord);

#endif
