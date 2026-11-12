/* ov001 row 0x022058b8: 272 bytes.
 *
 * What it does: 67 instructions; 5 call(s) to 0x0205f98c, 0x02205988, 0x02204ee0, +2 more; loops (back edge at +0x64); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (67 instructions, 5 calls, 5 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x10c -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x20 -> +0x3c
 *   branch +0x58 -> +0xf4
 *   branch +0xa4 -> +0xf4
 *   branch +0xbc -> +0xd0
 *   branch +0xd8 -> +0xf4
 *   back edge +0x100 -> +0x48
 *   test +0x54 cmp r0, r4
 *   test +0x84 cmp r0, #0
 *   test +0xb8 cmp r0, #1
 *   test +0xd0 cmp r8, #17
 *   test +0xd4 cmpne r8, #19
 *   test +0xfc cmp r7, #20
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022058b8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0205f98c(void);
extern void native_fn_02204ee0(void);
extern void native_fn_02048a60(void);


asm u32 native_ov001_022058b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    ldrsh r0, [r10, #38]
    ldr r5, [r10, #0x40]
    add r0, r0, #1
    strh r0, [r10, #38]
    ldrsh r0, [r10, #38]
    bics r0, r0, #7
    beq ov001_022058b8_L3c
    ldrsh r1, [r10, #24]
    mov r0, #0
    add r1, r1, #1
    and r1, r1, #1
    strh r1, [r10, #24]
    strh r0, [r10, #38]
ov001_022058b8_L3c:
    mov r7, #0
    mov r11, #12
    mvn r4, #0
ov001_022058b8_L48:
    mul r1, r7, r11
    ldrsb r0, [r5, r1]
    add r9, r5, r1
    cmp r0, r4
    beq ov001_022058b8_Lf4
    ldr r0, [r10, #0x1c]
    mov r1, r7
    bl native_fn_0205f98c
    mov r6, r0
    ldrb r1, [r6, #0x4]
    ldr r3, =0x66666667
    ldrsb r0, [r9, #1]
    sub r1, r1, #19
    smull r12, r2, r3, r1
    mov r8, r1, lsr #31
    cmp r0, #0
    subgt r0, r0, #2
    add r2, r8, r2, asr #3
    mov r3, #20
    smull r2, r8, r3, r2
    sub r2, r1, r2
    and r8, r2, #255
    strgtb r0, [r9, #0x1]
    bgt ov001_022058b8_Lf4
    ldr r0, [r6, #0x7c]
    orr r0, r0, #2
    str r0, [r6, #0x7c]
    ldrb r0, [r9, #0x6]
    cmp r0, #1
    bls ov001_022058b8_Ld0
    mov r0, r10
    mov r1, r7
    mov r2, #1
    bl native_fn_02204ee0
ov001_022058b8_Ld0:
    cmp r8, #17
    cmpne r8, #19
    bne ov001_022058b8_Lf4
    ldrsh r3, [r10, #24]
    ldrsh r1, [r9, #8]
    ldrsh r2, [r9, #10]
    mov r0, r6
    add r1, r3, r1
    bl native_fn_02048a60
ov001_022058b8_Lf4:
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #20
    blo ov001_022058b8_L48
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
