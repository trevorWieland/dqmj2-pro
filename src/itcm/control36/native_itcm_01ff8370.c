typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
#define FIELD(base, type, offset) (*(type)((s8 *)(base) + (offset)))
u32 native_itcm_01ff8370(u32 sourceOffset, u32 destination, u32 byteExtent) {
    u32 alignedOffset;
    s32 status;
    u32 commandMiddle;
    u32 control;
    s32 relativeOffset;
    u32 word;
    u32 alignment;

    control = *(u32 *)0x027FFE60;
    alignment = sourceOffset & 0x1FF;
    control = (control & ~0x07000000U) | 0xA1000000U;
    relativeOffset = 0 - alignment;
    do {

    } while (*(volatile u32 *)0x040001A4 & 0x80000000);
    FIELD((void *)0x040001A1, volatile u8 *, 0) = 0x80;
    alignedOffset = sourceOffset + relativeOffset;
    if (relativeOffset >= (s32) byteExtent) {
        return alignedOffset;
    }
    commandMiddle = alignedOffset >> 8;
    do {
        FIELD((void *)0x040001A1, volatile u8 *, 7) = 0xB7;
        FIELD((void *)0x040001A1, volatile u8 *, 8) = (s8) (alignedOffset >> 0x18);
        FIELD((void *)0x040001A1, volatile u8 *, 9) = (s8) (alignedOffset >> 0x10);
        FIELD((void *)0x040001A1, volatile u8 *, 0xA) = (s8) commandMiddle;
        FIELD((void *)0x040001A1, volatile u8 *, 0xB) = alignedOffset;
        FIELD((void *)0x040001A1, volatile u8 *, 0xC) = 0;
        FIELD((void *)0x040001A1, volatile u8 *, 0xD) = 0;
        FIELD((void *)0x040001A1, volatile u8 *, 0xE) = 0;
        FIELD((void *)0x040001A1, volatile u32 *, 3) = control;
read_status:
        status = FIELD((void *)0x040001A1, volatile u32 *, 3);
        if (status & 0x800000) {
            word = *(volatile u32 *)0x04100010;
            if ((relativeOffset >= 0) && (relativeOffset < (s32) byteExtent)) {
                *(u32 *)(destination + relativeOffset) = word;
            }
            relativeOffset += 4;
        }
        if (status & 0x80000000) {
            goto read_status;
        }
        commandMiddle += 2;
        alignedOffset += 0x200;
    } while (relativeOffset < (s32) byteExtent);
    return alignedOffset;
}
