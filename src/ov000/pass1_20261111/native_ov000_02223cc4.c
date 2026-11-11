/* Zero one word of a three-word record.
 *
 * Clears field `field` of record `index` in the 12-byte-stride table at
 * 0x0224665c. The record stride shows up as `mov #12` plus `mla`, so the table
 * is addressed as an array of three-word records. No value is returned; r0 is
 * only the zero being stored.
 * Unknowns: record semantics and the table's owner.
 */
typedef int s32;
typedef unsigned int u32;

typedef struct {
    u32 word[3];
} Rec3;

extern Rec3 native_data_ov000_0224665c[];

void native_ov000_02223cc4(s32 index, s32 field)
{
    native_data_ov000_0224665c[index].word[field] = 0;
}
