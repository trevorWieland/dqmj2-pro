/* Record refresh with a twelve-byte copy.
 *
 * Calls native_fn_02041f34 with the record, then copies the twelve-byte block at
 * record + 112 to record + 272 with the image's ldm/stm pair, and returns the
 * call's value. The call's result is parked in r12 across the copy.
 * Unknowns: what the two blocks hold.
 */
typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u32 word[3];
} Vec12;

extern u32 native_fn_02041f34(u8 *);

u32 native_ov000_021f3d04(u8 *record)
{
    u32 result = native_fn_02041f34(record);

    *(Vec12 *)(record + 272) = *(Vec12 *)(record + 112);
    return result;
}
