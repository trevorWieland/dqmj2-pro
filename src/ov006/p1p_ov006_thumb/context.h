#ifndef P1P_CONTEXT_H
#define P1P_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Mechanism indices for this batch:
   - 0x0221c170: pointer to the scene object (+0x84 subrecord);
   - 0x0221c188: pointer to the active handle (cleared after release);
   - 0x0221c1ac: pointer to the record whose +0x808 word is queued;
   - 0x0221c1e8: pointer to the 0x40-byte-stride table used by 0x02204974 and
     0x022049c4 (shared pool word);
   - 0x027e0000 + 0x3ff8: ITCM/DTCM control word (bit 0 set);
   - 0x020b4108: tail-call target of the 0x020b5890 setter. */

#endif
