/* Conditional record byte update (second field pair).
 *
 * Same shape as 0x21f3af8 with the gate at 0x278 and the updated byte at 0x1df
 * of a 636-byte record in the array rooted at the pointer stored at
 * 0x02236ed8 + 4. The -1 default is declared before the record pointer so it
 * stays in r12 for the whole body.
 * Unknowns: the gate's meaning; the record's owner.
 */
typedef unsigned char u8;
typedef int s32;

typedef struct {
    u8 pad0[0x1df];
    u8 slot;
    u8 pad1[0x278 - 0x1e0];
    u8 gate;
    u8 pad2[636 - 0x279];
} Rec636;

extern u8 native_data_ov000_02236ed8[];

s32 native_ov000_021f4174(s32 index, u8 value)
{
    s32 previous = -1;
    Rec636 *record = (Rec636 *)(*(u8 **)(native_data_ov000_02236ed8 + 4) + index * 636);

    if (record->gate) {
        previous = record->slot;
        record->slot = value;
    }
    return previous;
}
