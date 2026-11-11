/* Non-zero entry dispatch.
 *
 * Walks the six pointer-sized entries of the table given as the argument and
 * calls native_fn_021f0354 with the raw entry for each one whose low byte is
 * non-zero, stopping at the first zero entry. The image computes the byte test
 * with `lsl #24` / `asrs #24` but passes the untouched word.
 * Unknowns: what the entries point at.
 */
typedef signed char s8;
typedef int s32;
typedef unsigned int u32;

extern void native_fn_021f0354(u32);

void native_ov000_021f0394(u32 *table)
{
    s32 index = 0;

    do {
        u32 entry = table[index];

        if ((s8)entry == 0)
            return;
        native_fn_021f0354(entry);
        index++;
    } while (index < 6);
}
