/* ov001 row 0x021f5ea0: 488 bytes.
 *
 * What it does: 121 instructions; 8 call(s) to 0x0207afec, 0x021f5a84, 0x021f5a84, +5 more; loops (back edge at +0x18); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (121 instructions, 8 calls, 16 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x1e4 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x10 -> +0xb8
 *   branch +0x2c -> +0x64
 *   branch +0x40 -> +0x54
 *   branch +0x50 -> +0xb8
 *   branch +0x60 -> +0xb8
 *   branch +0x7c -> +0x90
 *   branch +0x8c -> +0xb8
 *   branch +0xa8 -> +0xb8
 *   branch +0xc4 -> +0xe8
 *   branch +0xf4 -> +0x120
 *   branch +0x108 -> +0x120
 *   branch +0x12c -> +0x14c
 *   branch +0x158 -> +0x1dc
 *   branch +0x164 -> +0x1a4
 *   branch +0x178 -> +0x1a4
 *   branch +0x1cc -> +0x1dc
 *   test +0x0c cmp r1, #0
 *   test +0x28 cmp r0, #1
 *   test +0x3c cmp r0, #0
 *   test +0x70 cmp r1, #0
 *   test +0x78 cmpne r1, #0
 *   test +0x98 cmp r0, #0
 *   test +0xc0 cmp r0, #10
 *   test +0xf0 cmp r1, #20
 *   test +0x104 cmp r0, #0
 *   test +0x128 cmp r1, #30
 *   test +0x13c cmp r1, #30
 *   test +0x154 cmp r1, #100
 *   test +0x160 cmp r1, #0
 *   test +0x174 cmp r0, #0
 *   test +0x1bc cmp r0, #0
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f5ea0; the literal pool and
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
extern void native_fn_021f5a84(void);
extern void native_fn_021f5c38(void);
extern void native_fn_021f5cc0(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbf98(void);


asm u32 native_ov001_021f5ea0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x43]
    cmp r1, #0
    bne ov001_021f5ea0_Lb8
    ldrh r0, [r0, #80]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021f5ea0_L64
    ldr r0, =0x0223989c
    ldrh r0, [r0, #80]
    bl native_fn_021f5a84
    cmp r0, #0
    beq ov001_021f5ea0_L54
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x43]
    b ov001_021f5ea0_Lb8
ov001_021f5ea0_L54:
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x43]
    b ov001_021f5ea0_Lb8
ov001_021f5ea0_L64:
    ldr r0, =0x0223989c
    ldr r2, [r0, #0x80]
    ldrb r1, [r2, #0x31c]
    cmp r1, #0
    ldrneb r1, [r2, #0x1ff]
    cmpne r1, #0
    bne ov001_021f5ea0_L90
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x43]
    b ov001_021f5ea0_Lb8
ov001_021f5ea0_L90:
    ldrh r0, [r0, #80]
    bl native_fn_021f5a84
    cmp r0, #0
    ldreq r0, =0x0223989c
    moveq r1, #100
    streqb r1, [r0, #0x43]
    beq ov001_021f5ea0_Lb8
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x43]
ov001_021f5ea0_Lb8:
    ldr r1, =0x0223989c
    ldrb r0, [r1, #0x43]
    cmp r0, #10
    bne ov001_021f5ea0_Le8
    ldrh r2, [r1, #80]
    ldr r0, [r1, #0x84]
    ldr r1, [r1, #0x80]
    mov r3, #1
    bl native_fn_021f5c38
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x43]
ov001_021f5ea0_Le8:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x43]
    cmp r1, #20
    bne ov001_021f5ea0_L120
    ldrh r1, [r0, #80]
    ldr r0, [r0, #0x80]
    bl native_fn_021f5cc0
    cmp r0, #0
    beq ov001_021f5ea0_L120
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x42]
    mov r1, #30
    strb r1, [r0, #0x43]
ov001_021f5ea0_L120:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x43]
    cmp r1, #30
    bne ov001_021f5ea0_L14c
    ldrb r1, [r0, #0x42]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x42]
    movhi r1, #100
    strhib r1, [r0, #0x43]
ov001_021f5ea0_L14c:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x43]
    cmp r1, #100
    bne ov001_021f5ea0_L1dc
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    bne ov001_021f5ea0_L1a4
    ldrh r0, [r0, #80]
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f5ea0_L1a4
    ldr r0, =0x0223989c
    mov r1, #8
    ldr r0, [r0, #0x84]
    mov r2, #0
    str r2, [sp]
    add r2, r0, #512
    ldrsb r2, [r2, #52]
    sub r3, r1, #9
    rsb r2, r2, #0
    bl native_fn_021dbf98
ov001_021f5ea0_L1a4:
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x43]
    ldrh r0, [r0, #80]
    mov r1, #16777216
    bl native_fn_0207b004
    cmp r0, #0
    ldreq r0, =0x0223989c
    moveq r1, #27
    streqb r1, [r0, #0x1b]
    beq ov001_021f5ea0_L1dc
    ldr r0, =0x0223989c
    mov r1, #14
    strb r1, [r0, #0x1b]
ov001_021f5ea0_L1dc:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
