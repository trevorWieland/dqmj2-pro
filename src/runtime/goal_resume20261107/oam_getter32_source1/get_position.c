#include "oam_getter.h"

u32 native_ov006_02202f98(u32 descriptorWord, s32 index, u32 outXWord, u32 outYWord) {
    OamDescriptorView *descriptor = (OamDescriptorView *)descriptorWord;
    OamEntryView *entries = descriptor->entries;
    u32 x;
    u32 y;

    x = (entries[index].attr01 & 0x01FF0000U) >> 16;
    *(u32 *)outXWord = x;
    y = entries[index].attr01 & 0xFFU;
    *(u32 *)outYWord = y;
    return y;
}
