/* Record probe and three-word payload copy (second table).
 *
 * Twin of 0x021e60a8 against the 0x02232568 table, the one that 0x021e60e0
 * allocates from. Same declaration order, 16-byte stride and offset-4 payload.
 * Unknowns: payload meaning and whether the two tables hold the same record type.
 */
typedef unsigned char u8;
typedef int s32;

typedef struct {
    s32 word_0;
    s32 word_4;
    s32 word_8;
} Payload;

extern u8 native_data_ov000_02232568[];

u8 *native_ov000_021e61c0(s32 index, Payload *out)
{
    u8 *result = 0;
    u8 *table = native_data_ov000_02232568;
    u8 *record = table + index * 16;

    if (record[0] != 0) {
        if (out != 0)
            *out = *(Payload *)(record + 4);
        result = record + 4;
    }
    return result;
}
