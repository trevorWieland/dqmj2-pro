/* ov001 row 0x02213254: 436 bytes.
 *
 * What it does: 108 instructions; 10 call(s) to 0x02008e0c, 0x021f949c, 0x02048260, +7 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (108 instructions, 10 calls, 21 branches, 10 back edges, 1 literal slot).
 *
 *   pool +0x1b0 -> constant 0x0000011a (image word 0x0000011a)
 *   branch +0x24 -> +0x198
 *   branch +0x28 -> +0x40
 *   branch +0x2c -> +0x64
 *   branch +0x30 -> +0xbc
 *   branch +0x34 -> +0xbc
 *   branch +0x38 -> +0x17c
 *   branch +0x3c -> +0x190
 *   branch +0x60 -> +0x198
 *   branch +0x74 -> +0x198
 *   branch +0x88 -> +0x198
 *   branch +0xb8 -> +0x198
 *   branch +0xc8 -> +0xd8
 *   branch +0xd4 -> +0xe0
 *   branch +0xe4 -> +0x110
 *   branch +0x10c -> +0x198
 *   branch +0x114 -> +0x128
 *   branch +0x124 -> +0x198
 *   branch +0x150 -> +0x160
 *   back edge +0x16c -> +0x13c
 *   branch +0x178 -> +0x198
 *   branch +0x18c -> +0x198
 *   branch +0x19c -> +0x1a8
 *   back edge +0x1a4 -> +0x00
 *   test +0x18 cmp r2, #5
 *   test +0x68 cmp r0, #0
 *   test +0x84 cmp r1, #0
 *   test +0xc0 cmp r2, #2
 *   test +0xcc cmp r0, #1
 *   test +0xd8 cmp r0, #0
 *   test +0xe0 cmp r1, #0
 *   test +0xf4 cmp r0, #2
 *   test +0x110 cmp r2, #2
 *   test +0x14c cmp r1, #0
 *   test +0x168 cmp r5, #24
 *   test +0x198 cmp r4, #0
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213254; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_021f949c(void);
extern void native_fn_02048260(void);
extern void native_fn_02212a64(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02212f14(void);


asm u32 native_ov001_02213254 (register u32 a0)
{
ov001_02213254_L0:
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    ldr r1, [r7, #0x38]
    ldr r2, [r7, #0x34]
    ldr r5, [r7, #0x40]
    mov r6, r1, lsl #5
    cmp r2, #5
    mov r4, #0
    addls pc, pc, r2, lsl #2
    b ov001_02213254_L198
    b ov001_02213254_L40
    b ov001_02213254_L64
    b ov001_02213254_Lbc
    b ov001_02213254_Lbc
    b ov001_02213254_L17c
    b ov001_02213254_L190
ov001_02213254_L40:
    add r0, r6, #512
    mov r1, r5
    add r0, r0, #83886080
    mov r2, #32
    bl native_fn_02008e0c
    mov r0, #1
    strh r0, [r7, #38]
    str r0, [r7, #0x34]
    b ov001_02213254_L198
ov001_02213254_L64:
    ldr r0, [r5, #0x24]
    cmp r0, #0
    moveq r0, #5
    streq r0, [r7, #0x34]
    beq ov001_02213254_L198
    ldrsh r1, [r7, #38]
    sub r0, r1, #1
    strh r0, [r7, #38]
    cmp r1, #0
    bge ov001_02213254_L198
    ldr r0, =0x0000011a
    mov r1, #1
    bl native_fn_021f949c
    add r0, r5, #10
    add r1, r6, #8
    mov r2, #2
    bl native_fn_02048260
    mov r0, r4
    strb r0, [r7, #0x24]
    mov r0, #2
    str r0, [r7, #0x34]
    b ov001_02213254_L198
ov001_02213254_Lbc:
    mov r1, r4
    cmp r2, #2
    ldrsb r0, [r7, #36]
    bne ov001_02213254_Ld8
    cmp r0, #1
    movgt r1, #1
    b ov001_02213254_Le0
ov001_02213254_Ld8:
    cmp r0, #0
    movle r1, #1
ov001_02213254_Le0:
    cmp r1, #0
    bne ov001_02213254_L110
    mov r0, r7
    bl native_fn_02212a64
    ldr r0, [r7, #0x34]
    cmp r0, #2
    ldrsb r0, [r7, #36]
    addeq r0, r0, #2
    streqb r0, [r7, #0x24]
    subne r0, r0, #1
    strneb r0, [r7, #0x24]
    b ov001_02213254_L198
ov001_02213254_L110:
    cmp r2, #2
    bne ov001_02213254_L128
    mov r0, #3
    str r0, [r7, #0x34]
    mov r4, #1
    b ov001_02213254_L198
ov001_02213254_L128:
    add r0, r5, #8
    add r1, r6, #8
    mov r2, #2
    bl native_fn_02048260
    mov r5, #0
ov001_02213254_L13c:
    ldr r0, [r7, #0x1c]
    mov r1, r5
    bl native_fn_0205f98c
    ldr r1, [r0, #0x84]
    cmp r1, #0
    beq ov001_02213254_L160
    ldrsh r1, [r7, #20]
    ldrsh r2, [r7, #22]
    bl native_fn_02048a60
ov001_02213254_L160:
    add r0, r5, #1
    and r5, r0, #255
    cmp r5, #24
    blo ov001_02213254_L13c
    mov r0, #4
    str r0, [r7, #0x34]
    b ov001_02213254_L198
ov001_02213254_L17c:
    mov r0, #25
    strh r0, [r7, #38]
    mov r0, #1
    str r0, [r7, #0x34]
    b ov001_02213254_L198
ov001_02213254_L190:
    mov r1, #1
    bl native_fn_02212f14
ov001_02213254_L198:
    cmp r4, #0
    beq ov001_02213254_L1a8
    mov r0, r7
    bl ov001_02213254_L0
ov001_02213254_L1a8:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
