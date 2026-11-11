/* Gate byte check, byte store and record action.
 *
 * Indexes the 716-byte records at 0x0223526c, returns 0 when the gate byte 0x274
 * is clear, otherwise writes the caller's byte to 0x27a, runs
 * native_fn_02042f4c on the record and reports 1.
 * Unknowns: what the stored byte selects.
 */
typedef unsigned char u8;
typedef int s32;
typedef unsigned int u32;

typedef struct {
    u8 pad0[0x274];
    u8 gate;
    u8 pad1[0x27a - 0x275];
    u8 field;
    u8 pad2[716 - 0x27b];
} Rec716;

extern Rec716 native_data_ov000_0223526c[];
extern void native_fn_02042f4c(Rec716 *);

u32 native_ov000_021e8e94(s32 index, u8 value)
{
    Rec716 *record = &native_data_ov000_0223526c[index];

    if (record->gate == 0)
        return 0;
    record->field = value;
    native_fn_02042f4c(record);
    return 1;
}
