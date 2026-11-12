/* ov006 row 0x021da064: 248 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf4 -> constant 0x3ff80000 (image word 0x3ff80000)
 *   branch +0x34 -> +0x9c
 *   branch +0x74 -> +0x88
 *   back edge +0x8c -> +0x64
 *   back edge +0xa8 -> +0x2c
 *   branch +0xc0 -> +0xec
 *   test +0x30 cmp r0, #0
 *   test +0x70 cmp lr, #0
 *   test +0x80 cmp r12, r3
 *   test +0xa0 cmp r4, #3
 *   test +0xac cmp r5, #1
 *   test +0xbc cmp r5, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021da064; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02067748(void);
extern void native_fn_020679ac(void);
extern void native_fn_02067968(void);
extern void native_fn_02024504(void);
extern void native_fn_02024540(void);
extern void native_fn_020243e0(void);


asm u32 native_ov006_021da064 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r7, r0
    mov r10, #0
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    bl native_fn_020679ac
    mov r5, r10
    mov r6, r0
    mov r4, r5
    mov r9, r10
    mov r8, #15
ov006_021da064_L2c:
    ldrsh r0, [r7, #24]
    cmp r0, #0
    beq ov006_021da064_L9c
    bl native_fn_02067748
    ldr r0, [r0, #0x4]
    bl native_fn_02067968
    ldrsh r2, [r7, #24]
    ldrb r3, [r7, #0x1a]
    mov r1, r9
    add r2, r2, r2, lsl #1
    add r3, r3, r2
    mov r2, r8
    add r0, r0, r3, lsl #1
    add r5, r5, #1
ov006_021da064_L64:
    add r3, r6, r2, lsl #2
    ldrh lr, [r3, #2]
    mov r3, r2, lsl #2
    cmp lr, #0
    beq ov006_021da064_L88
    ldrh r12, [r0]
    ldrh r3, [r6, r3]
    cmp r12, r3
    movls r1, lr
ov006_021da064_L88:
    subs r2, r2, #1
    bpl ov006_021da064_L64
    add r0, r10, r1
    mov r0, r0, lsl #16
    mov r10, r0, lsr #16
ov006_021da064_L9c:
    add r4, r4, #1
    cmp r4, #3
    add r7, r7, #132
    blt ov006_021da064_L2c
    cmp r5, #1
    addeq r0, r10, r10, lsl #1
    moveq r0, r0, lsl #16
    moveq r10, r0, lsr #16
    cmp r5, #2
    bne ov006_021da064_Lec
    mov r0, r10
    bl native_fn_02024504
    mov r3, r1
    mov r2, r0
    ldr r1, =0x3ff80000
    mov r0, #0
    bl native_fn_02024540
    bl native_fn_020243e0
    mov r0, r0, lsl #16
    mov r10, r0, lsr #16
ov006_021da064_Lec:
    mov r0, r10
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
