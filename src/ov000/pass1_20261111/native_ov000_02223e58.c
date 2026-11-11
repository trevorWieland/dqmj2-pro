/* Stride-3 table byte probe (second table).
 *
 * Sign-extends the byte at `base + index * 3 + 0x022465a0`; identical shape to
 * 0x02223d70 with the table twelve bytes further along.
 * Unknowns: whether `base` is a section base and which record group this is.
 */
typedef signed char s8;
typedef int s32;
typedef unsigned int u32;

extern s8 native_data_ov000_022465a0[];

s8 native_ov000_02223e58(s32 index, s8 *base)
{
    return base[index * 3 + (u32)native_data_ov000_022465a0];
}
