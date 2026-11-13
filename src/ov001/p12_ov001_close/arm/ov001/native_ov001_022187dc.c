/* ov001 row 0x022187DC: 160 bytes.
 *
 * ov001_any_active_slot_compare_022187dc: Returns 1 when any of three active records satisfies the selected comparison.
 *
 * Evidence: Loops three 0x440-byte records, skips inactive with 021DB8D0, reads signed byte [record + offset + 0x24C], and returns 1 for mode 0 (>=), 1 (==), 2 (<=).
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


asm u32 ov001_any_active_slot_compare_022187dc (register u8 *records, register u32 offset, register s32 value, register u32 mode)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    mov r7, r2
    mov r6, r3
    add r5, r8, r1
    mov r4, #0
ov001_022187dc_L18:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022187dc_L84
    cmp r6, #0
    bne ov001_022187dc_L48
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r0, r7
    blt ov001_022187dc_L84
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov001_022187dc_L48:
    cmp r6, #1
    bne ov001_022187dc_L68
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r7, r0
    bne ov001_022187dc_L84
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov001_022187dc_L68:
    cmp r6, #2
    bne ov001_022187dc_L84
    add r0, r5, #512
    ldrsb r0, [r0, #44]
    cmp r0, r7
    movle r0, #1
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
ov001_022187dc_L84:
    add r4, r4, #1
    cmp r4, #3
    add r8, r8, #1088
    add r5, r5, #1088
    blt ov001_022187dc_L18
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
