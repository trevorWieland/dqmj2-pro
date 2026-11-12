/* ov001 row 0x021fafec: 496 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x1e0 -> constant 0x02239a14 (image word 0x02239a14)
 *   pool +0x1e4 -> constant 0x02239b40 (image word 0x02239b40)
 *   pool +0x1e8 -> native_fn_021f9540 (image word 0x021f9540)
 *   pool +0x1ec -> native_fn_021f9558 (image word 0x021f9558)
 *   branch +0x14 -> +0x38
 *   branch +0x24 -> +0x1d4
 *   branch +0x34 -> +0x1d4
 *   branch +0x3c -> +0xa8
 *   branch +0x4c -> +0x84
 *   branch +0x58 -> +0x1d4
 *   branch +0x80 -> +0x1d4
 *   branch +0x8c -> +0x1d4
 *   branch +0xa4 -> +0x1d4
 *   branch +0xac -> +0xe8
 *   branch +0xc0 -> +0x1d4
 *   branch +0xe4 -> +0x1d4
 *   branch +0xec -> +0x11c
 *   branch +0x100 -> +0x1d4
 *   branch +0x118 -> +0x1d4
 *   branch +0x120 -> +0x188
 *   back edge +0x16c -> +0x160
 *   branch +0x184 -> +0x1d4
 *   branch +0x18c -> +0x1d4
 *   branch +0x198 -> +0x1d4
 *   test +0x10 cmp r1, #0
 *   test +0x20 cmp r0, #0
 *   test +0x38 cmp r1, #5
 *   test +0x48 cmp r1, #1000
 *   test +0x54 cmp r0, #0
 *   test +0x6c cmp r1, #0
 *   test +0x88 cmp r0, #0
 *   test +0xa8 cmp r1, #10
 *   test +0xbc cmp r2, #0
 *   test +0xe8 cmp r1, #11
 *   test +0xfc cmp r2, #0
 *   test +0x11c cmp r1, #100
 *   test +0x188 cmp r1, #110
 *   test +0x194 cmp r0, #0
 *   test +0x1ac cmp r0, r2
 *   17 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fafec; the literal pool and
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

extern void native_fn_02212adc(void);
extern void native_fn_02212af8(void);
extern void native_fn_02212b44(void);
extern void native_fn_02212b28(void);
extern void native_fn_02212ac8(void);
extern void native_fn_021f9540(void);
extern void native_fn_021f9558(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern void native_fn_0205fd60(void);
extern void native_fn_0203d294(void);
extern void native_fn_021e3544(void);


asm u32 native_ov001_021fafec (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0xf]
    cmp r1, #0
    bne ov001_021fafec_L38
    ldrsb r0, [r0, #16]
    bl native_fn_02212adc
    cmp r0, #0
    beq ov001_021fafec_L1d4
    ldr r0, =0x02239a14
    mov r1, #5
    strb r1, [r0, #0xf]
    b ov001_021fafec_L1d4
ov001_021fafec_L38:
    cmp r1, #5
    bne ov001_021fafec_La8
    ldrsh r1, [r0, #38]
    ldrsb r0, [r0, #16]
    cmp r1, #1000
    bge ov001_021fafec_L84
    bl native_fn_02212af8
    cmp r0, #0
    beq ov001_021fafec_L1d4
    ldr r0, =0x02239a14
    mov r1, #10
    strb r1, [r0, #0xf]
    ldrsh r1, [r0, #38]
    cmp r1, #0
    movne r1, #90
    strneh r1, [r0, #42]
    moveq r1, #0
    streqh r1, [r0, #42]
    b ov001_021fafec_L1d4
ov001_021fafec_L84:
    bl native_fn_02212b44
    cmp r0, #0
    beq ov001_021fafec_L1d4
    ldr r0, =0x02239a14
    mov r1, #11
    strb r1, [r0, #0xf]
    mov r1, #50
    strh r1, [r0, #42]
    b ov001_021fafec_L1d4
ov001_021fafec_La8:
    cmp r1, #10
    bne ov001_021fafec_Le8
    ldrsh r2, [r0, #42]
    sub r1, r2, #1
    strh r1, [r0, #42]
    cmp r2, #0
    bgt ov001_021fafec_L1d4
    ldrsb r0, [r0, #16]
    bl native_fn_02212b28
    ldr r0, =0x02239a14
    ldrsb r0, [r0, #16]
    bl native_fn_02212ac8
    ldr r0, =0x02239a14
    mov r1, #100
    strb r1, [r0, #0xf]
    b ov001_021fafec_L1d4
ov001_021fafec_Le8:
    cmp r1, #11
    bne ov001_021fafec_L11c
    ldrsh r2, [r0, #42]
    sub r1, r2, #1
    strh r1, [r0, #42]
    cmp r2, #0
    bgt ov001_021fafec_L1d4
    ldrsb r0, [r0, #16]
    bl native_fn_02212ac8
    ldr r0, =0x02239a14
    mov r1, #100
    strb r1, [r0, #0xf]
    b ov001_021fafec_L1d4
ov001_021fafec_L11c:
    cmp r1, #100
    bne ov001_021fafec_L188
    mov r0, #18
    str r0, [sp]
    mov r0, #8192
    str r0, [sp, #0x4]
    mov r3, #2
    str r3, [sp, #0x8]
    mov r3, #0
    ldr r0, =0x02239b40
    ldr r1, =native_fn_021f9540
    ldr r2, =native_fn_021f9558
    str r3, [sp, #0xc]
    bl native_fn_0205fc10
    ldr lr, =0x02239b40
    mov r4, r0
    mov r12, #13
ov001_021fafec_L160:
    ldmia r4!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne ov001_021fafec_L160
    ldr r0, =0x02239b40
    bl native_fn_0205fd0c
    ldr r0, =0x02239a14
    mov r1, #110
    strb r1, [r0, #0xf]
    b ov001_021fafec_L1d4
ov001_021fafec_L188:
    cmp r1, #110
    bne ov001_021fafec_L1d4
    bl native_fn_0205fd60
    cmp r0, #0
    bne ov001_021fafec_L1d4
    mov r0, #1000
    bl native_fn_0203d294
    ldr r1, =0x02239a14
    ldrsh r2, [r1, #38]
    cmp r0, r2
    movlt r0, #13
    movge r0, #14
    strb r0, [r1, #0xa]
    mov r0, #0
    mov r1, #1
    bl native_fn_021e3544
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0xf]
ov001_021fafec_L1d4:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
