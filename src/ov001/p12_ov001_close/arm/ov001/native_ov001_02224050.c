/* ov001 row 0x02224050: 84 bytes.
 *
 * ov001_pick_random_candidate_02224050: Picks a random occupied slot from a three-word candidate set and clears the rest.
 *
 * Evidence: Calls 0203D294(3) (the shared RNG accessor) until candidates[index] != 0, then clears every other word; callers pass the 12-byte block filled by 02223FE8/02226BDC/02224570.
 * Touches: three-word candidate block; random service 0x0203D294.
 * Remaining unknowns: Whether the selected word is an ability id, item id or skill id is not established.
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

extern void ov001_count_candidates_02223f20(void);
extern void native_fn_0203d294(void);


asm u32 ov001_pick_random_candidate_02224050 (register u32 *candidates)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl ov001_count_candidates_02223f20
    cmp r0, #0
    ble ov001_02224050_L30
    mov r4, #3
ov001_02224050_L18:
    mov r0, r4
    bl native_fn_0203d294
    ldr r1, [r5, r0, lsl #2]
    cmp r1, #0
    beq ov001_02224050_L18
    b ov001_02224050_L34
ov001_02224050_L30:
    mov r0, #0
ov001_02224050_L34:
    mov r2, #0
    mov r1, r2
ov001_02224050_L3c:
    cmp r0, r2
    strne r1, [r5, r2, lsl #2]
    add r2, r2, #1
    cmp r2, #3
    blt ov001_02224050_L3c
    ldmia sp!, {r3, r4, r5, pc}
}
