/* ov005 row 0x021db5d0: 296 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x11c -> constant 0x022550ff (image word 0x022550ff)
 *   pool +0x120 -> constant 0x91a2b3c5 (image word 0x91a2b3c5)
 *   pool +0x124 -> constant 0x88888889 (image word 0x88888889)
 *   back edge +0x30 -> +0x18
 *   test +0x3c cmp r5, r0
 *   6 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov005.bin at 0x021db5d0; the literal pool and
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
extern void native_fn_021ddec4(void);


asm u32 native_ov005_021db5d0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #32
    mov r5, r0
    add r2, sp, #0
    mov r1, #4
    mov r0, #0
ov005_021db5d0_L18:
    strh r0, [r2]
    strh r0, [r2, #2]
    strh r0, [r2, #4]
    strh r0, [r2, #6]
    add r2, r2, #8
    subs r1, r1, #1
    bne ov005_021db5d0_L18
    ldr r0, =0x022550ff
    mov r4, #0
    cmp r5, r0
    movhi r5, r0
    ldr r0, =0x91a2b3c5
    add r1, sp, #0
    umull r2, r0, r5, r0
    mov r0, r0, lsr #11
    mov r2, #32
    mov r3, #4
    bl native_fn_020877bc
    add r0, r4, #4
    and r2, r0, #255
    add r0, r2, #1
    and r4, r0, #255
    ldr r0, =0x91a2b3c5
    mov r12, r5
    umull r0, r5, r12, r0
    mov r1, r4, lsl #1
    mov r0, r2, lsl #1
    rsb r2, r1, #32
    add lr, sp, #0
    mov r1, #58
    mov r5, r5, lsr #11
    mov r3, #3600
    strh r1, [lr, r0]
    umull r0, r1, r3, r5
    sub r5, r12, r0
    ldr r0, =0x88888889
    add r1, lr, r4, lsl #1
    umull r3, r0, r5, r0
    mov r0, r0, lsr #5
    mov r3, #2
    bl native_fn_0208791c
    add r0, r4, #2
    and r0, r0, #255
    mov r1, r0, lsl #1
    add r0, r0, #1
    and r2, r0, #255
    ldr r0, =0x88888889
    mov r4, #58
    add r3, sp, #0
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
    mov r0, #9
    add r1, sp, #0
    bl native_fn_021ddec4
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
}
