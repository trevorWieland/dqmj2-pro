/* ov000 row 0x022082f4: 836 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x334 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x338 -> constant 0x022550ff (image word 0x022550ff)
 *   pool +0x33c -> constant 0x91a2b3c5 (image word 0x91a2b3c5)
 *   pool +0x340 -> constant 0x022384e8 (image word 0x022384e8)
 *   branch +0x28 -> +0x38
 *   back edge +0x48 -> +0x10
 *   branch +0x9c -> +0xe0
 *   back edge +0xdc -> +0xa4
 *   back edge +0x194 -> +0x17c
 *   branch +0x2b4 -> +0x328
 *   branch +0x2d0 -> +0x30c
 *   back edge +0x324 -> +0x2c0
 *   test +0x24 cmp r0, #0
 *   test +0x44 cmp r5, #2
 *   test +0x98 cmp r0, #0
 *   test +0xd8 cmp r4, r0
 *   test +0x1ac cmp r1, r4
 *   test +0x2b0 cmp r0, #0
 *   test +0x2cc cmp r0, #100
 *   test +0x320 cmp r6, r0
 *   24 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022082f4; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_020852c8(void);
extern void native_fn_02206c6c(void);
extern void native_fn_0220617c(void);
extern void native_fn_02206a64(void);
extern void native_fn_0220820c(void);
extern void native_fn_02206ab8(void);
extern void native_fn_021df3bc(void);
extern void native_fn_020877bc(void);
extern void native_fn_0208791c(void);
extern void native_fn_02206a20(void);
extern void native_fn_02206d44(void);
extern void native_fn_02065818(void);
extern void native_fn_02085200(void);


asm u32 native_ov000_022082f4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #44
    mov r5, #0
    mov r4, #1
ov000_022082f4_L10:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r0, [r0]
    cmp r0, #0
    beq ov000_022082f4_L38
    ldr r0, [r0, #0x4]
    mov r1, r4
    bl native_fn_020852c8
ov000_022082f4_L38:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #2
    blt ov000_022082f4_L10
    bl native_fn_02206c6c
    add r1, sp, #8
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    bl native_fn_0220617c
    mov r5, r0
    mov r4, #16
    add r2, sp, #8
    add r1, r5, #4
    mov r0, #8
    mov r3, #1
    strh r4, [sp, #8]
    bl native_fn_02206a64
    ldrsh r0, [sp, #10]
    mov r4, #0
    add r0, r0, #16
    strh r0, [sp, #10]
    ldrb r0, [r5, #0x5d]
    cmp r0, #0
    ble ov000_022082f4_Le0
    add r6, r5, #24
ov000_022082f4_La4:
    add r0, r5, r4, lsl #1
    add r1, r5, r4
    ldrh r0, [r0, #84]
    ldrb r2, [r1, #0x5a]
    ldrsh r3, [sp, #10]
    mov r1, r6
    bl native_fn_0220820c
    ldrsh r0, [sp, #10]
    add r4, r4, #1
    add r6, r6, #20
    add r0, r0, #16
    strh r0, [sp, #10]
    ldrb r0, [r5, #0x5d]
    cmp r4, r0
    blt ov000_022082f4_La4
ov000_022082f4_Le0:
    add r1, sp, #8
    str r1, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #8
    mov r1, #5
    mov r2, #2
    mov r3, #58
    bl native_fn_02206ab8
    ldrsh r1, [sp, #8]
    add r0, r1, r0
    strh r0, [sp, #8]
    ldrb r0, [r5, #0x5e]
    bl native_fn_021df3bc
    add r1, sp, #8
    str r1, [sp]
    mov r2, #0
    str r2, [sp, #0x4]
    ldrb r3, [r0, #0x2]
    mov r0, #8
    mov r1, #6
    bl native_fn_02206ab8
    mov r0, #16
    ldrsh r1, [sp, #10]
    strh r0, [sp, #8]
    mov r2, #2
    add r0, r1, #16
    strh r0, [sp, #10]
    add r1, sp, #8
    str r1, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r0, #8
    mov r1, #5
    mov r3, #10
    bl native_fn_02206ab8
    add r2, sp, #12
    mov r1, #4
    mov r0, #0
ov000_022082f4_L17c:
    strh r0, [r2]
    strh r0, [r2, #2]
    strh r0, [r2, #4]
    strh r0, [r2, #6]
    add r2, r2, #8
    subs r1, r1, #1
    bne ov000_022082f4_L17c
    ldr r2, [r5]
    ldr r0, =0x88888889
    ldr r1, =0x022550ff
    umull r0, r4, r2, r0
    mov r4, r4, lsr #4
    cmp r1, r4
    movlo r4, r1
    ldr r0, =0x91a2b3c5
    mov r6, #0
    umull r2, r0, r4, r0
    add r1, sp, #12
    mov r0, r0, lsr #11
    mov r2, #32
    mov r3, #4
    bl native_fn_020877bc
    add r0, r6, #4
    and r2, r0, #255
    add r0, r2, #1
    and r6, r0, #255
    ldr r0, =0x91a2b3c5
    mov lr, r4
    umull r0, r4, r14, r0
    add r3, sp, #12
    mov r1, r6, lsl #1
    mov r7, r2, lsl #1
    mov r0, #58
    rsb r2, r1, #32
    mov r4, r4, lsr #11
    mov r12, #3600
    strh r0, [r3, r7]
    add r1, r3, r6, lsl #1
    umull r0, r3, r12, r4
    sub r4, lr, r0
    ldr r0, =0x88888889
    mov r3, #2
    umull r12, r0, r4, r0
    mov r0, r0, lsr #5
    bl native_fn_0208791c
    add r0, r6, #2
    and r0, r0, #255
    mov r1, r0, lsl #1
    add r0, r0, #1
    and r2, r0, #255
    ldr r0, =0x88888889
    mov r6, #58
    add r3, sp, #12
    strh r6, [r3, r1]
    umull r1, r0, r4, r0
    add r1, r3, r2, lsl #1
    mov r2, r2, lsl #1
    mov r0, r0, lsr #5
    mov r6, #60
    umull r0, r3, r6, r0
    rsb r2, r2, #32
    sub r0, r4, r0
    mov r3, #2
    bl native_fn_0208791c
    mov r0, #80
    strh r0, [sp, #8]
    mov r0, #8
    add r1, sp, #12
    add r2, sp, #8
    mov r3, #0
    bl native_fn_02206a20
    mov r0, #144
    strh r0, [sp, #8]
    mov r0, #16
    strh r0, [sp, #10]
    ldrb r0, [r5, #0x5d]
    mov r6, #0
    cmp r0, #0
    ble ov000_022082f4_L328
    ldr r7, =0x022384e8
    mov r4, r6
ov000_022082f4_L2c0:
    add r0, r5, r6
    ldrb r0, [r0, #0x5a]
    bic r0, r0, #128
    cmp r0, #100
    blt ov000_022082f4_L30c
    mov r0, r4
    bl native_fn_02206d44
    ldrsh r3, [sp, #8]
    ldrsh r12, [r7, #26]
    ldrsh r2, [r7, #28]
    ldrsh r1, [sp, #10]
    add r3, r3, #7
    add r3, r12, r3, asr #3
    add r2, r2, r1, asr #3
    mov r1, r3, lsl #24
    mov r2, r2, lsl #24
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_02065818
ov000_022082f4_L30c:
    ldrsh r0, [sp, #10]
    add r6, r6, #1
    add r0, r0, #16
    strh r0, [sp, #10]
    ldrb r0, [r5, #0x5d]
    cmp r6, r0
    blt ov000_022082f4_L2c0
ov000_022082f4_L328:
    bl native_fn_02085200
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, pc}
}
