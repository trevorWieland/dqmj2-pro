/* Packed byte pair split and sentinel test.
 *
 * Splits a packed signed word into its low two bytes, stores each as a word
 * through the two out pointers, then reports whether both stored values avoid
 * the 255 sentinel (1 = both usable, 0 = at least one sentinel). The image
 * reloads both values from memory, so the test reads through the pointers.
 * Unknowns: what the packed word and the sentinel mean.
 */
typedef int s32;
typedef unsigned int u32;

u32 native_ov000_02209bc0(s32 packed, u32 *low, u32 *high)
{
    *low = packed & 0xff;
    *high = (packed >> 8) & 0xff;
    if (*low != 255 && *high != 255)
        return 1;
    return 0;
}
