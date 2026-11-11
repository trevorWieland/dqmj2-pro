/* Stride-708 gate byte write and tail call.
 *
 * Sets byte 0x1e5 of record `index` in the table at 0x02238634 to 1 when the
 * second argument is zero and to 0 otherwise, then tail-calls
 * native_fn_ov000_0221089c with the record pointer and the untouched argument
 * (the image keeps the arguments in r0/r1 and branches through the callee
 * literal in r12). The record pointer is formed with `mla` into r0.
 * Unknowns: what the gate byte enables; what the callee does with the record.
 */
typedef unsigned char u8;
typedef int s32;
typedef unsigned int u32;

typedef struct {
    u8 pad0[0x1e5];
    u8 gate;
    u8 pad1[708 - 0x1e6];
} Rec708;

extern Rec708 native_data_ov000_02238634[];
extern u32 native_fn_ov000_0221089c(Rec708 *, u32);

u32 native_ov000_022108dc(s32 index, u32 flag)
{
    Rec708 *record = &native_data_ov000_02238634[index];

    record->gate = flag == 0 ? 1 : 0;
    return native_fn_ov000_0221089c(record, flag);
}
