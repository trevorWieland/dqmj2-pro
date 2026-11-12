/* ov001 row 0x02224570: 204 bytes.
 *
 * ov001_filter_highest_priority_candidates_02224570: Keeps only the candidate slots whose 022244A0 priority equals the maximum.
 *
 * Evidence: Two passes over three candidates: first takes max 022244A0(record, mode), second clears every slot below it; only copies the block back when a non-zero candidate remains.
 * Touches: three-word candidate block; three 0x440-byte records; 0x022244A0 priority function.
 * Remaining unknowns: The priority function's scale and game meaning are not established.
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

extern void native_fn_02008e0c(void);
extern void native_fn_022244a0(void);
extern void ov001_count_candidates_02223f20(void);


asm u32 ov001_filter_highest_priority_candidates_02224570 (register u32 *candidates, register u8 *records, register u32 mode)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r5, r1
    mov r4, r2
    add r1, sp, #0
    mov r2, #12
    mov r6, r0
    mov r9, #0
    bl native_fn_02008e0c
    mov r10, r5
    mov r8, r9
    add r7, sp, #0
ov001_02224570_L30:
    ldr r0, [r7, r8, lsl #2]
    cmp r0, #0
    beq ov001_02224570_L50
    mov r0, r10
    mov r1, r4
    bl native_fn_022244a0
    cmp r0, r9
    movgt r9, r0
ov001_02224570_L50:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_02224570_L30
    mov r8, #0
    mov r10, r8
    add r7, sp, #0
ov001_02224570_L6c:
    ldr r0, [r7, r8, lsl #2]
    cmp r0, #0
    beq ov001_02224570_L8c
    mov r0, r5
    mov r1, r4
    bl native_fn_022244a0
    cmp r0, r9
    strlt r10, [r7, r8, lsl #2]
ov001_02224570_L8c:
    add r8, r8, #1
    cmp r8, #3
    add r5, r5, #1088
    blt ov001_02224570_L6c
    add r0, sp, #0
    bl ov001_count_candidates_02223f20
    mov r4, r0
    cmp r4, #0
    ble ov001_02224570_Lc0
    add r0, sp, #0
    mov r1, r6
    mov r2, #12
    bl native_fn_02008e0c
ov001_02224570_Lc0:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
