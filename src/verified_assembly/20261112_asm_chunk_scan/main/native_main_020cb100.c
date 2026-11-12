/* main row 0x020cb100: 460 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x1bc -> constant 0x021d6620 (image word 0x021d6620)
 *   pool +0x1c0 -> constant 0x021d6630 (image word 0x021d6630)
 *   pool +0x1c4 -> native_fn_020cba74 (image word 0x020cba74)
 *   pool +0x1c8 -> native_fn_020cbb28 (image word 0x020cbb28)
 *   branch +0x20 -> +0x44
 *   branch +0x50 -> +0x6c
 *   branch +0x78 -> +0x124
 *   branch +0x88 -> +0x124
 *   branch +0x9c -> +0x124
 *   back edge +0x10c -> +0x100
 *   branch +0x134 -> +0x174
 *   branch +0x148 -> +0x174
 *   branch +0x180 -> +0x1b0
 *   branch +0x1a4 -> +0x1ac
 *   test +0x1c cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x74 cmp r0, #0
 *   test +0x84 cmp r0, #42
 *   test +0x130 cmp r0, r2
 *   test +0x17c cmp r0, #42
 *   19 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020cb100; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_020cb490(void);
extern void native_fn_020cbc3c(void);
extern void native_fn_020cb770(void);
extern void native_fn_020cba74(void);
extern void native_fn_020cbb28(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern void native_fn_020cbbd8(void);
extern void native_fn_02062144(void);
extern void native_fn_020cb2fc(void);
extern void native_fn_020cbb64(void);


asm u32 native_main_020cb100 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    bl native_fn_02061944
    ldr r1, =0x021d6620
    mov r4, r0
    ldr r0, [r1, #0xc]
    mov r5, #0
    cmp r0, #0
    beq main_020cb100_L44
    strb r5, [r1]
    ldr r0, =0x021d6630
    str r5, [r1, #0xc]
    ldrsb r3, [r0, #209]
    mov r2, #1
    orr r3, r3, #8
    strb r3, [r0, #0xd1]
    str r2, [r1, #0x8]
main_020cb100_L44:
    ldr r0, =0x021d6620
    ldrb r0, [r0, #0x4]
    cmp r0, #0
    beq main_020cb100_L6c
    bl native_fn_020cb490
    bl native_fn_020cbc3c
    bl native_fn_020cb770
    ldr r0, =0x021d6620
    mov r1, #0
    strb r1, [r0, #0x4]
main_020cb100_L6c:
    ldr r0, =0x021d6620
    ldr r0, [r0, #0x8]
    cmp r0, #0
    beq main_020cb100_L124
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    bne main_020cb100_L124
    ldr r0, =0x021d6630
    ldrsb r1, [r0, #209]
    mov r2, r1, lsl #31
    movs r2, r2, asr #31
    bne main_020cb100_L124
    bic r1, r1, #1
    mov r3, #0
    strb r3, [r0, #0xd0]
    orr r1, r1, #1
    strb r1, [r0, #0xd1]
    ldrsb r1, [r0, #209]
    mov r12, #18
    mov r6, #8192
    bic r1, r1, #2
    strb r1, [r0, #0xd1]
    ldrsb lr, [r0, #209]
    mov r2, #2
    ldr r1, =native_fn_020cba74
    bic lr, lr, #8
    strb lr, [r0, #0xd1]
    str r12, [sp]
    str r6, [sp, #0x4]
    str r2, [sp, #0x8]
    ldr r2, =native_fn_020cbb28
    str r3, [sp, #0xc]
    bl native_fn_0205fc10
    ldr lr, =0x021d6630
    mov r6, r0
    mov r12, #13
main_020cb100_L100:
    ldmia r6!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne main_020cb100_L100
    ldr r0, =0x021d6630
    bl native_fn_0205fd0c
    ldr r0, =0x021d6620
    mov r1, #0
    str r1, [r0, #0x8]
main_020cb100_L124:
    ldr r1, =0x021d6620
    ldrb r2, [r1, #0x1]
    ldrb r0, [r1, #0x2]
    cmp r0, r2
    beq main_020cb100_L174
    ldr r0, =0x021d6630
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    bne main_020cb100_L174
    strb r2, [r1, #0x2]
    mov r0, #1
    str r0, [r1, #0xc]
    strb r0, [r1, #0x4]
    bl native_fn_020cbbd8
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    bl native_fn_020cb2fc
main_020cb100_L174:
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    beq main_020cb100_L1b0
    ldr r1, =0x021d6620
    mov r2, #0
    strb r2, [r1, #0x2]
    ldr r0, =0x021d6630
    strb r2, [r1, #0x1]
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    beq main_020cb100_L1ac
    bl native_fn_020cbb64
main_020cb100_L1ac:
    mov r5, #1
main_020cb100_L1b0:
    mov r0, r5
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
