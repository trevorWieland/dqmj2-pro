/* main row 0x020d28cc: 328 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x13c -> constant 0x022550ff (image word 0x022550ff)
 *   pool +0x140 -> constant 0x91a2b3c5 (image word 0x91a2b3c5)
 *   pool +0x144 -> constant 0x88888889 (image word 0x88888889)
 *   back edge +0x34 -> +0x1c
 *   test +0x40 cmp r5, r0
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020d28cc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020877bc(void);
extern void native_fn_0208791c(void);
extern void native_fn_0204ab98(void);


asm u32 native_main_020d28cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #40
    mov r6, r0
    mov r5, r1
    add r2, sp, #8
    mov r1, #4
    mov r0, #0
main_020d28cc_L1c:
    strh r0, [r2]
    strh r0, [r2, #2]
    strh r0, [r2, #4]
    strh r0, [r2, #6]
    add r2, r2, #8
    subs r1, r1, #1
    bne main_020d28cc_L1c
    ldr r0, =0x022550ff
    add r1, sp, #4
    cmp r5, r0
    movhi r5, r0
    ldr r0, =0x91a2b3c5
    mov r4, #0
    umull r2, r0, r5, r0
    strh r4, [r1]
    strh r4, [r1, #2]
    add r1, sp, #8
    mov r0, r0, lsr #11
    mov r2, #32
    mov r3, #4
    bl native_fn_020877bc
    add r0, r4, #4
    and r2, r0, #255
    add r0, r2, #1
    and r4, r0, #255
    ldr r0, =0x91a2b3c5
    mov lr, r5
    umull r0, r5, r14, r0
    add r3, sp, #8
    mov r12, r2, lsl #1
    mov r0, #58
    mov r1, r4, lsl #1
    strh r0, [r3, r12]
    rsb r2, r1, #32
    mov r5, r5, lsr #11
    mov r12, #3600
    add r1, r3, r4, lsl #1
    umull r0, r3, r12, r5
    sub r5, lr, r0
    ldr r0, =0x88888889
    mov r3, #2
    umull r12, r0, r5, r0
    mov r0, r0, lsr #5
    bl native_fn_0208791c
    add r0, r4, #2
    and r0, r0, #255
    mov r1, r0, lsl #1
    add r0, r0, #1
    and r2, r0, #255
    ldr r0, =0x88888889
    mov r4, #58
    add r3, sp, #8
    strh r4, [r3, r1]
    umull r1, r0, r5, r0
    add r1, r3, r2, lsl #1
    mov r2, r2, lsl #1
    mov r0, r0, lsr #5
    mov r4, #60
    umull r0, r3, r4, r0
    rsb r2, r2, #32
    sub r0, r5, r0
    mov r3, #2
    bl native_fn_0208791c
    mov r0, r6, lsl #24
    mov r2, #1
    mov r0, r0, asr #24
    add r1, sp, #4
    add r3, sp, #8
    str r2, [sp]
    bl native_fn_0204ab98
    add sp, sp, #40
    ldmia sp!, {r4, r5, r6, pc}
}
