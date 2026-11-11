/* Three-word record table accessor.
 *
 * Returns the word at record `index`, field `field` of the 12-byte-stride table
 * at 0x0224665c. The record stride is materialised as `mov #12` plus `mla`, so
 * the table is indexed as an array of three-word records rather than as a flat
 * word array. Callers in the roster lane declare the result as a void pointer
 * and pass record 0/1 with a field index.
 * Unknowns: record semantics and the table's owner.
 */
typedef int s32;
typedef unsigned int u32;

typedef struct {
    u32 word[3];
} Rec3;

extern Rec3 native_data_ov000_0224665c[];

void *native_ov000_02223d40(s32 index, s32 field)
{
    return (void *)native_data_ov000_0224665c[index].word[field];
}
