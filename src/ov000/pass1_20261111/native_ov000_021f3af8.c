/* Conditional record byte update.
 *
 * Indexes the 636-byte record array rooted at the pointer stored at
 * 0x02236ed8 + 4 and updates byte 0x1e3 of the record when its gate byte 0x278
 * is non-zero. Returns the previous byte, or -1 when the gate is clear. The -1
 * default is declared before the record pointer, which is the order that puts it
 * in r12 with a final `mov r0, r12`; declaring it after the pointer makes mwcc
 * fold the default into an r0 overwrite and loses four bytes.
 * Unknowns: the gate's meaning; the record's owner.
 */
typedef unsigned char u8;
typedef int s32;

typedef struct {
    u8 pad0[0x1e3];
    u8 slot;
    u8 pad1[0x278 - 0x1e4];
    u8 gate;
    u8 pad2[636 - 0x279];
} Rec636;

extern u8 native_data_ov000_02236ed8[];

s32 native_ov000_021f3af8(s32 index, u8 value)
{
    s32 previous = -1;
    Rec636 *record = (Rec636 *)(*(u8 **)(native_data_ov000_02236ed8 + 4) + index * 636);

    if (record->gate) {
        previous = record->slot;
        record->slot = value;
    }
    return previous;
}
