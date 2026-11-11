/* Claim the first free slot for a matching record.
 *
 * Scans four slots: a slot counts when it is still zero and the value matches
 * the signed halfword at `table + index * 2 + 2`. The claim stores 1 in the slot
 * and bumps the signed-byte counter. The image folds the whole conjunction into
 * predicated `eq` instructions and returns after the claim.
 * Unknowns: what the table and the counter track.
 */
typedef signed char s8;
typedef short s16;
typedef int s32;
typedef unsigned char u8;
typedef unsigned int u32;

void native_ov000_02228d10(u8 *table, s16 value, u32 *slots, s8 *counter)
{
    s32 index;

    index = 0;
    do {
        if (slots[index] == 0 && value == *(s16 *)(table + index * 2 + 2)) {
            slots[index] = 1;
            *counter = *counter + 1;
            return;
        }
        index++;
    } while (index < 4);
}
