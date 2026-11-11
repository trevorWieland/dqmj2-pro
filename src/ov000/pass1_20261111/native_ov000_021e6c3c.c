/* Record header and two 12-byte payload copies.
 *
 * Copies the twelve-byte payload from `payload_hi` into the record's second
 * payload slot (offset 16) and the one from `payload_lo` into its first slot
 * (offset 4), then stores the halfword tag at offset 2 and clears the halfword
 * at offset 0. The image copies the higher slot first, so the assignments are in
 * that order.
 * Unknowns: what the two payload slots mean; the record's owner.
 */
typedef unsigned short u16;
typedef unsigned int u32;

typedef struct {
    u32 word[3];
} Vec12;

typedef struct {
    u16 tag0;
    u16 tag1;
    Vec12 low;
    Vec12 high;
} Rec;

void native_ov000_021e6c3c(Rec *record, Vec12 *payload_lo, Vec12 *payload_hi, u16 tag)
{
    record->high = *payload_hi;
    record->low = *payload_lo;
    record->tag1 = tag;
    record->tag0 = 0;
}
