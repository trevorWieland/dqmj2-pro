/* Sub-object payload copy.
 *
 * Queries the object with the caller's argument and returns null when the query
 * fails. On success the result is the object's sub-block at offset 32, which is
 * also copied through the optional out pointer (the image copies it with an
 * ldm/stm pair guarded by `cmpne`).
 * Unknowns: what the sub-block holds.
 */
typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u32 word[3];
} Vec12;

extern u32 native_fn_021e7764(u32);

u8 *native_ov000_021e77c8(u32 arg, Vec12 *out)
{
    u8 *result = 0;
    u32 object = native_fn_021e7764(arg);

    if (object != 0) {
        result = (u8 *)object + 32;
        if (out != 0)
            *out = *(Vec12 *)result;
    }
    return result;
}
