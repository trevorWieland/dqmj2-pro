/* ov001 row 0x021F1354: 164 bytes.
 *
 * ov001_begin_state_transition_021f1354: Starts a guarded state transition: sets state bit 2, issues a 4-argument service call and two mode callbacks.
 *
 * Evidence: Returns immediately if state->+0x18 bit 2 is already set; otherwise calls 02085284(state+0x3C, arg0&0xFF, arg1&0xFF, (s16)arg2), sets bit 2, calls 02086B14(state, 22), 02086B24(state, 24 or 4) and 02085420(state, 0).
 * Touches: ov001 state 0x02238F58 -> +4; service calls 02085284/02086B14/02086B24/02085420.
 * Remaining unknowns: The transition's target screen and the service call's contract are not established.
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

extern void native_fn_02085284(void);
extern void native_fn_02086b14(void);
extern void native_fn_02086b24(void);
extern void native_fn_02085420(void);


asm u32 ov001_begin_state_transition_021f1354 (register u32 arg0, register u32 arg1, register u32 arg2, register u32 arg3)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =0x02238f58
    mov r5, r0
    ldr r12, [r4, #0x4]
    mov r4, r3
    ldr r0, [r12, #0x18]
    mov lr, r1
    and r0, r0, #2
    cmp r0, #2
    ldmeqia sp!, {r3, r4, r5, pc}
    mov r3, r2, lsl #16
    add r0, r12, #60
    and r1, r5, #255
    and r2, lr, #255
    mov r3, r3, lsr #16
    bl native_fn_02085284
    ldr r0, =0x02238f58
    mov r1, #22
    ldr r3, [r0, #0x4]
    ldr r2, [r3, #0x18]
    orr r2, r2, #2
    str r2, [r3, #0x18]
    ldr r0, [r0, #0x4]
    bl native_fn_02086b14
    cmp r4, #1
    bne ov001_021f1354_L7c
    ldr r0, =0x02238f58
    mov r1, #24
    ldr r0, [r0, #0x4]
    bl native_fn_02086b24
    b ov001_021f1354_L8c
ov001_021f1354_L7c:
    ldr r0, =0x02238f58
    mov r1, #4
    ldr r0, [r0, #0x4]
    bl native_fn_02086b24
ov001_021f1354_L8c:
    ldr r0, =0x02238f58
    mov r1, #0
    ldr r0, [r0, #0x4]
    bl native_fn_02085420
    ldmia sp!, {r3, r4, r5, pc}
}
