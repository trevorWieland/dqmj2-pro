#ifndef P1O_CONTEXT_H
#define P1O_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Mechanism indices for this batch:
   - 0x0221c0d4 / 0x0221c100: frame counters with 0x78 wrap and reset via 0x21f52cc;
   - 0x0221c0d8: pointer to the active frame record (word +4 -> record, record +8 -> list);
   - 0x0221c134: pointer to the active queue (first word is the item);
   - 0x0221c140: pointer to the active slot record (+0x10/+0x12 are 16-bit spans,
     +0x1a mode byte, +0x1c/+0x1d pair, +0x1e flag);
   - 0x0221c14c: pointer +0x9c -> active sub-record;
   - 0x0221c15c: pointer to the count-record (+0x1d counter, wraps at 8);
   - 0x0221c160: pointer to the 16-bit flag array (+2 word, entries at +0xe + (n-1)*0x1e);
   - 0x027fffa8: main-RAM status word, bit 15 is the flag read by three rows here. */

#endif
