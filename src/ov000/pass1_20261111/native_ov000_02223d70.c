/* Stride-3 table byte probe.
 *
 * Sign-extends the byte at `base + index * 3 + 0x02246594`; the table address
 * is added to the caller's base pointer, so the measured literal is the data
 * address 0x02246594 itself.
 * Unknowns: whether `base` is a section base and which record group this is.
 */
typedef signed char s8;
typedef int s32;
typedef unsigned int u32;

extern s8 native_data_ov000_02246594[];

s8 native_ov000_02223d70(s32 index, s8 *base)
{
    return base[index * 3 + (u32)native_data_ov000_02246594];
}
