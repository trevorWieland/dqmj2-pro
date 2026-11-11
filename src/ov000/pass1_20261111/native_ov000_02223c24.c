/* Word accumulator over a flat word table.
 *
 * Adds `value` to entry `index` of the table at 0x022465a8 and returns the new
 * total (the image keeps the sum in r1, stores it, then moves it to r0, so the
 * slot is updated through a pointer and the sum is the expression value).
 * Unknowns: what the counter feeds; the table's extent.
 */
typedef int s32;
typedef unsigned int u32;

extern u32 native_data_ov000_022465a8[];

u32 native_ov000_02223c24(s32 index, u32 value)
{
    u32 *slot = &native_data_ov000_022465a8[index];

    return *slot += value;
}
