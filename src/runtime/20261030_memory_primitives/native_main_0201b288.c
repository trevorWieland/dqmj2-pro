typedef unsigned int u32;
typedef unsigned char u8;
void native_main_0201b288(void *destination, int value, u32 count) {
    u8 *bytes = destination;
    u32 fill = (u8)value;
    u32 alignment;
    u32 blocks;
    u32 *words;
    if (count >= 32) {
        alignment = (0U - (u32)bytes) & 3;
        if (alignment) {
            count -= alignment;
            do {
                *bytes++ = fill;
            } while (--alignment);
        }
        if (fill) {
            fill |= fill << 24 | fill << 16 | fill << 8;
        }
        words = (u32 *)bytes;
        blocks = count >> 5;
        if (blocks) {
            do {
                words[0] = fill;
                words[1] = fill;
                words[2] = fill;
                words[3] = fill;
                words[4] = fill;
                words[5] = fill;
                words[6] = fill;
                words[7] = fill;
                words += 8;
            } while (--blocks);
        }
        blocks = (count & 31) >> 2;
        if (blocks) {
            do {
                *words++ = fill;
            } while (--blocks);
        }
        bytes = (u8 *)words;
        count &= 3;
    }
    if (count) {
        do {
            *bytes++ = fill;
        } while (--count);
    }
}
