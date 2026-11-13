/* ov001 row 0x0221873C: 160 bytes.
 *
 * ov001_all_active_slots_compare_0221873c: Returns 1 when every active record satisfies the selected comparison, 0 otherwise.
 *
 * Evidence: Loops three 0x440-byte records; mode 0 fails on <, mode 1 fails on !=, mode 2 fails on >; inactive records are ignored and a fully inactive set returns 1 at the last index.
 * Touches: three 0x440-byte records; signed byte +0x24C; 021DB8D0 predicate.
 * Remaining unknowns: What the signed byte at +0x24C represents is not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void ov001_record_is_active_021db8d0(void);


asm u32 ov001_all_active_slots_compare_0221873c (register u8 *records, register u32 offset, register s32 value, register u32 mode)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r2
    mov r6, r3
    add r5, r8, r1
    mov r4, #0
ov001_0221873c_L18:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221873c_L78
    cmp r6, #0
    bne ov001_0221873c_L44
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r0, r7
    blt ov001_0221873c_L98
    b ov001_0221873c_L78
ov001_0221873c_L44:
    cmp r6, #1
    bne ov001_0221873c_L60
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r7, r0
    bne ov001_0221873c_L98
    b ov001_0221873c_L78
ov001_0221873c_L60:
    cmp r6, #2
    bne ov001_0221873c_L78
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r0, r7
    bgt ov001_0221873c_L98
ov001_0221873c_L78:
    cmp r4, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    add r4, r4, #1
    cmp r4, #3
    add r8, r8, #1088
    add r5, r5, #1088
    blt ov001_0221873c_L18
ov001_0221873c_L98:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
