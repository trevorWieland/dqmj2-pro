/* Record probe and three-word payload copy (first table).
 *
 * The result, table and record are declared in that order: the image materialises
 * the null result first, keeps the table literal in r2 and the computed record in
 * r3. When the record's state byte is set, copies the payload at offset 4 into the
 * caller's 12-byte block and returns its address.
 * Unknowns: payload meaning; the difference from the twin at 0x021e61c0.
 */
typedef unsigned char u8;
typedef int s32;

typedef struct {
    s32 word_0;
    s32 word_4;
    s32 word_8;
} Payload;

extern u8 native_data_ov000_02232668[];

u8 *native_ov000_021e60a8(s32 index, Payload *out)
{
    u8 *result = 0;
    u8 *table = native_data_ov000_02232668;
    u8 *record = table + index * 16;

    if (record[0] != 0) {
        if (out != 0)
            *out = *(Payload *)(record + 4);
        result = record + 4;
    }
    return result;
}
