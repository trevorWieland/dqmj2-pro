/* main row 0x020d0ca8: 408 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x188 -> constant 0x021d6bb4 (image word 0x021d6bb4)
 *   pool +0x18c -> constant 0x021d6bcc (image word 0x021d6bcc)
 *   pool +0x190 -> native_fn_020d1404 (image word 0x020d1404)
 *   pool +0x194 -> native_fn_020d1594 (image word 0x020d1594)
 *   branch +0x20 -> +0x30
 *   branch +0x28 -> +0x11c
 *   branch +0x2c -> +0x150
 *   branch +0x64 -> +0xf0
 *   branch +0x74 -> +0xf0
 *   back edge +0xe4 -> +0xd8
 *   branch +0xf8 -> +0x10c
 *   branch +0x118 -> +0x150
 *   branch +0x12c -> +0x150
 *   branch +0x138 -> +0x150
 *   branch +0x15c -> +0x17c
 *   branch +0x170 -> +0x178
 *   test +0x1c cmp r0, #0
 *   test +0x24 cmp r0, #1
 *   test +0x60 cmp r1, #42
 *   test +0xf4 cmp r0, #0
 *   test +0x158 cmp r0, #42
 *   11 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020d0ca8; the literal pool and
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
extern void native_fn_02062328(void);
extern void native_fn_02062144(void);
extern void native_fn_020d1154(void);
extern void native_fn_020d1404(void);
extern void native_fn_020d1594(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern void native_fn_02041930(void);
extern void native_fn_02041510(void);
extern void native_fn_020d15d0(void);


asm u32 native_main_020d0ca8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    bl native_fn_02061944
    ldr r1, =0x021d6bb4
    mov r4, r0
    ldrb r0, [r1, #0x2]
    mov r5, #0
    cmp r0, #0
    beq main_020d0ca8_L30
    cmp r0, #1
    beq main_020d0ca8_L11c
    b main_020d0ca8_L150
main_020d0ca8_L30:
    bl native_fn_02062328
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, r5
    bl native_fn_02062144
    bl native_fn_020d1154
    ldr r0, =0x021d6bcc
    add r1, r4, #512
    ldrsb r2, [r0, #209]
    orr r2, r2, #8
    strb r2, [r0, #0xd1]
    ldrsb r1, [r1, #108]
    cmp r1, #42
    bne main_020d0ca8_Lf0
    ldrsb r1, [r0, #209]
    mov r2, r1, lsl #31
    movs r2, r2, asr #31
    bne main_020d0ca8_Lf0
    bic r1, r1, #1
    mov r3, r5
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
    ldr r1, =native_fn_020d1404
    bic lr, lr, #8
    strb lr, [r0, #0xd1]
    str r12, [sp]
    str r6, [sp, #0x4]
    str r2, [sp, #0x8]
    ldr r2, =native_fn_020d1594
    str r3, [sp, #0xc]
    bl native_fn_0205fc10
    ldr lr, =0x021d6bcc
    mov r6, r0
    mov r12, #13
main_020d0ca8_Ld8:
    ldmia r6!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs r12, r12, #1
    bne main_020d0ca8_Ld8
    ldr r0, =0x021d6bcc
    bl native_fn_0205fd0c
main_020d0ca8_Lf0:
    bl native_fn_02041930
    cmp r0, #0
    beq main_020d0ca8_L10c
    mov r0, #0
    mov r1, #2
    mov r2, #30
    bl native_fn_02041510
main_020d0ca8_L10c:
    ldr r0, =0x021d6bb4
    mov r1, #1
    strb r1, [r0, #0x2]
    b main_020d0ca8_L150
main_020d0ca8_L11c:
    ldr r0, =0x021d6bcc
    ldrsb r1, [r0, #209]
    mov r2, r1, lsl #31
    movs r2, r2, asr #31
    beq main_020d0ca8_L150
    mov r1, r1, lsl #29
    movs r1, r1, asr #31
    beq main_020d0ca8_L150
    bl native_fn_0205fd0c
    ldr r0, =0x021d6bcc
    ldrsb r1, [r0, #209]
    bic r1, r1, #4
    strb r1, [r0, #0xd1]
main_020d0ca8_L150:
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    beq main_020d0ca8_L17c
    ldr r0, =0x021d6bcc
    ldrsb r0, [r0, #209]
    mov r0, r0, lsl #31
    movs r0, r0, asr #31
    beq main_020d0ca8_L178
    bl native_fn_020d15d0
main_020d0ca8_L178:
    mov r5, #1
main_020d0ca8_L17c:
    mov r0, r5
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
