#include "../context.h"

/* 0x021f0f60: seed the four work words with the caller's value. */
void native_ov001_021f0f60(u32 value) {
    s8 i = 0;
    do {
        ((u32 *)native_data_ov001_02238f6c)[i] = value;
        i++;
    } while (i < 4);
}
