typedef unsigned char u8;
typedef unsigned int u32;
typedef signed char s8;
typedef struct NNSiG2dBitReader {
    const u8 * src;
    s8 availableBits;
    u8 bits;
    u8 padding_[2];
} NNSiG2dBitReader;
u32 native_main_02034ab8(NNSiG2dBitReader * reader, int nBits);
static inline void BitReaderReload (NNSiG2dBitReader * reader)
{
    reader->bits = *(reader->src)++;
    reader->availableBits = 8;
}
u32 native_main_02034ab8 (NNSiG2dBitReader * reader, int nBits)
{
    u32 val = reader->bits;
    int nAvlBits = reader->availableBits;
    if (nAvlBits < nBits) {
        int lack = nBits - nAvlBits;
        val <<= lack;
        BitReaderReload(reader);
        val |= native_main_02034ab8(reader, lack);
    } else {
        val >>= (nAvlBits - nBits);
        reader->availableBits = (s8)(nAvlBits - nBits);
    }
    val &= 0xFF >> (8 - nBits);
    return val;
}
