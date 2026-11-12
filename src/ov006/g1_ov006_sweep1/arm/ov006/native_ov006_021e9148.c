/* ov006 row 0x021E9148: 172 bytes.
 *
 * ov006_commit_mode_transition_021e9148: Commits a mode transition: updates the selected mode field, clears the pending flag and returns success.
 *
 * Evidence: Guards on 021E7E90; on mode 0 calls 0205FA4C(0x02218E60, 1) and 021E90C0, otherwise updates record+0x80 bit 3; calls 0204B61C(0x02218E18, 0), 021E8044(state->+0x5C) with 3/4, then clears state +4 and returns 1.
 * Touches: state 0x02218D90 (+0x5C, +4); record +0x80; UI callbacks 021E7E90/021E90C0/021E8044.
 * Remaining unknowns: The transition target and the +0x80 bit 3 meaning are not established.
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

extern void native_fn_021e7e90(void);
extern void native_fn_0205fa4c(void);
extern void native_fn_021e90c0(void);
extern void native_fn_02049ae4(void);
extern u8 native_data3_02218d90[];
extern void native_fn_0204b61c(void);
extern void native_fn_021e8044(void);


asm u32 ov006_commit_mode_transition_021e9148 (register void *state, register u32 mode)
{
    stmdb sp!, {r4, lr}
    mov r4, r1
    bl native_fn_021e7e90
    cmp r0, #0
    beq ov006_021e9148_L98
    cmp r4, #0
    bne ov006_021e9148_L30
    ldr r0, =0x02218e60
    mov r1, #1
    bl native_fn_0205fa4c
    bl native_fn_021e90c0
    b ov006_021e9148_L60
ov006_021e9148_L30:
    bl native_fn_02049ae4
    cmp r0, #0
    ldrne r2, [r0, #0x4]
    cmpne r2, #0
    beq ov006_021e9148_L60
    ldr r0, =native_data3_02218d90
    ldr r1, [r2, #0x80]
    ldr r0, [r0, #0x3c]
    bic r1, r1, #8
    mov r0, r0, lsl #31
    orr r0, r1, r0, lsr #28
    str r0, [r2, #0x80]
ov006_021e9148_L60:
    ldr r0, =0x02218e18
    mov r1, #0
    bl native_fn_0204b61c
    ldr r1, =native_data3_02218d90
    cmp r4, #0
    movne r0, #4
    ldr r1, [r1, #0x5c]
    moveq r0, #3
    bl native_fn_021e8044
    ldr r0, =native_data3_02218d90
    mov r1, #0
    str r1, [r0, #0x4]
    mov r0, #1
    ldmia sp!, {r4, pc}
ov006_021e9148_L98:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
