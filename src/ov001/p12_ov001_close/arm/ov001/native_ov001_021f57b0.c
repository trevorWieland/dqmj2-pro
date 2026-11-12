/* ov001 row 0x021f57b0: 724 bytes.
 *
 * What it does: 177 instructions; 22 call(s) to 0x0207afec, 0x0202ac08, 0x021f521c, +19 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill (177 instructions, 22 calls, 22 branches, 18 back edges, 4 literal slots).
 *
 *   pool +0x2c4 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x2c8 -> constant 0x0223992c (image word 0x0223992c)
 *   pool +0x2cc -> constant 0x00000119 (image word 0x00000119)
 *   pool +0x2d0 -> constant 0x0000010d (image word 0x0000010d)
 *   branch +0x20 -> +0x30
 *   branch +0x2c -> +0x64
 *   branch +0x3c -> +0x50
 *   branch +0x4c -> +0x5c
 *   branch +0x58 -> +0x68
 *   branch +0x60 -> +0x68
 *   branch +0x74 -> +0x110
 *   branch +0xb0 -> +0xbc
 *   branch +0xd0 -> +0x104
 *   branch +0x11c -> +0x184
 *   branch +0x130 -> +0x160
 *   branch +0x140 -> +0x184
 *   branch +0x14c -> +0x184
 *   branch +0x15c -> +0x184
 *   branch +0x16c -> +0x184
 *   branch +0x190 -> +0x2b8
 *   branch +0x1a4 -> +0x25c
 *   branch +0x1d8 -> +0x238
 *   branch +0x228 -> +0x238
 *   back edge +0x244 -> +0x1cc
 *   branch +0x258 -> +0x2b0
 *   branch +0x26c -> +0x2a4
 *   branch +0x27c -> +0x294
 *   branch +0x290 -> +0x2a4
 *   branch +0x2a0 -> +0x2b0
 *   test +0x1c cmp r2, #0
 *   test +0x28 cmp r2, #0
 *   test +0x48 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0xa8 cmp r2, #0
 *   test +0xcc cmp r0, #0
 *   test +0x118 cmp r1, #10
 *   test +0x124 cmp r1, #0
 *   test +0x13c cmp r1, #30
 *   test +0x148 cmp r0, #0
 *   test +0x168 cmp r1, #40
 *   test +0x174 cmp r0, #0
 *   test +0x18c cmp r1, #100
 *   test +0x1a0 cmp r2, #0
 *   test +0x1d4 cmp r0, #0
 *   test +0x224 cmp r0, r11
 *   test +0x23c cmp r7, #3
 *   test +0x268 cmp r0, #0
 *   test +0x278 cmp r1, #0
 *   test +0x28c cmp r0, #54
 *   1 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f57b0; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021f521c(void);
extern void native_fn_021e215c(void);
extern void native_fn_021f2120(void);
extern void native_fn_02212290(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021f2304(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021dc940(void);
extern void native_fn_021f4210(void);
extern void native_fn_0207b004(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f57b0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #36
    ldr r0, =0x0223989c
    ldrh r0, [r0, #80]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    ldrb r2, [r1, #0x10]
    cmp r2, #0
    beq ov001_021f57b0_L30
    ldrb r2, [r1, #0x13]
    cmp r2, #0
    beq ov001_021f57b0_L64
ov001_021f57b0_L30:
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    beq ov001_021f57b0_L50
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x8]
    cmp r0, #0
    beq ov001_021f57b0_L5c
ov001_021f57b0_L50:
    ldr r0, =0x0223989c
    ldr r4, [r0, #0x80]
    b ov001_021f57b0_L68
ov001_021f57b0_L5c:
    mov r4, #0
    b ov001_021f57b0_L68
ov001_021f57b0_L64:
    ldr r4, [r1, #0x80]
ov001_021f57b0_L68:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x47]
    cmp r0, #0
    bne ov001_021f57b0_L110
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    add r1, sp, #32
    str r1, [sp]
    ldr r0, =0x0223989c
    mov r1, r4
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x84]
    mov r3, #1
    bl native_fn_021f521c
    ldr r2, [sp, #0x20]
    ldr r1, =0x0223989c
    cmp r2, #0
    strb r0, [r1, #0x45]
    beq ov001_021f57b0_Lbc
    ldr r0, [r1, #0x84]
    bl native_fn_021e215c
ov001_021f57b0_Lbc:
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x46]
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    beq ov001_021f57b0_L104
    mov r0, r4
    mov r1, #176
    bl native_fn_021f2120
    mov r0, r4
    mov r1, #249
    bl native_fn_021f2120
    ldr r1, =0x00000119
    mov r0, r4
    bl native_fn_021f2120
    ldr r1, =0x0000010d
    mov r0, r4
    bl native_fn_021f2120
ov001_021f57b0_L104:
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x47]
ov001_021f57b0_L110:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x47]
    cmp r1, #10
    bne ov001_021f57b0_L184
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    ldrb r1, [r0, #0x46]
    add r2, r1, #1
    bne ov001_021f57b0_L160
    and r1, r2, #255
    strb r2, [r0, #0x46]
    cmp r1, #30
    bls ov001_021f57b0_L184
    bl native_fn_02212290
    cmp r0, #0
    bne ov001_021f57b0_L184
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x47]
    b ov001_021f57b0_L184
ov001_021f57b0_L160:
    and r1, r2, #255
    strb r2, [r0, #0x46]
    cmp r1, #40
    bls ov001_021f57b0_L184
    bl native_fn_02212290
    cmp r0, #0
    ldreq r0, =0x0223989c
    moveq r1, #100
    streqb r1, [r0, #0x47]
ov001_021f57b0_L184:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x47]
    cmp r1, #100
    bne ov001_021f57b0_L2b8
    mov r1, #0
    strb r1, [r0, #0x47]
    ldrb r2, [r0, #0x10]
    cmp r2, #0
    beq ov001_021f57b0_L25c
    ldrb r0, [r0, #0x11]
    bl native_fn_021db438
    mov r10, r0
    mov r7, #0
    ldr r4, =0x0223989c
    ldr r11, =0x00000119
    mov r8, r10
    mov r6, r7
    add r5, sp, #28
ov001_021f57b0_L1cc:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f57b0_L238
    ldrh r1, [r4, #80]
    mov r0, r8
    mov r2, #0
    bl native_fn_021f2304
    str r6, [sp]
    stmib sp, {r5, r6}
    str r6, [sp, #0xc]
    str r6, [sp, #0x10]
    str r6, [sp, #0x14]
    str r6, [sp, #0x18]
    add r0, r0, r0, lsl #4
    add r9, r10, r0, lsl #6
    ldrh r0, [r4, #80]
    ldr r1, [r4, #0x84]
    mov r2, r9
    mov r3, r6
    bl native_fn_021e1a60
    ldrh r0, [sp, #28]
    cmp r0, r11
    bne ov001_021f57b0_L238
    mov r0, r9
    mov r1, #27
    bl native_fn_021dc940
ov001_021f57b0_L238:
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #1088
    blt ov001_021f57b0_L1cc
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
    b ov001_021f57b0_L2b0
ov001_021f57b0_L25c:
    ldrh r0, [r0, #80]
    mov r1, #16777216
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f57b0_L2a4
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x45]
    cmp r1, #0
    bne ov001_021f57b0_L294
    ldrh r0, [r0, #80]
    bl native_fn_0207afec
    ldrb r0, [r0, #0x21]
    cmp r0, #54
    beq ov001_021f57b0_L2a4
ov001_021f57b0_L294:
    ldr r0, =0x0223989c
    mov r1, #14
    strb r1, [r0, #0x1b]
    b ov001_021f57b0_L2b0
ov001_021f57b0_L2a4:
    ldr r0, =0x0223989c
    mov r1, #27
    strb r1, [r0, #0x1b]
ov001_021f57b0_L2b0:
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
ov001_021f57b0_L2b8:
    mov r0, #0
    add sp, sp, #36
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
