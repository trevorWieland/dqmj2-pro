/* ov001 row 0x021f2230: 212 bytes.
 *
 * What it does: 52 instructions; 3 call(s) to 0x021dbb14, 0x021dbb9c, 0x022168e8; loops (back edge at +0x24); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (52 instructions, 3 calls, 5 branches, 2 back edges, 1 literal slot).
 *
 *   pool +0xd0 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x1c -> +0x60
 *   branch +0x2c -> +0x40
 *   branch +0x3c -> +0x60
 *   branch +0x50 -> +0x60
 *   branch +0x6c -> +0xac
 *   test +0x18 cmp r3, #0
 *   test +0x28 cmp r0, #0
 *   test +0x40 cmp r6, #0
 *   test +0x68 cmp r0, #10
 *   test +0x80 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0x9c cmp r6, #0
 *   test +0xb4 cmp r1, #100
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f2230; the literal pool and
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

extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);
extern void native_fn_022168e8(void);


asm u32 native_ov001_021f2230 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r3, =0x0223989c
    mov r5, r0
    ldrb r3, [r3, #0x17]
    mov r6, r1
    mov r4, r2
    cmp r3, #0
    bne ov001_021f2230_L60
    mov r1, r4
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_021f2230_L40
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x17]
    b ov001_021f2230_L60
ov001_021f2230_L40:
    cmp r6, #0
    ldreq r0, =0x0223989c
    moveq r1, #100
    streqb r1, [r0, #0x17]
    beq ov001_021f2230_L60
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x17]
ov001_021f2230_L60:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x17]
    cmp r0, #10
    bne ov001_021f2230_Lac
    mov r0, r5
    mov r1, r4
    mov r6, #0
    bl native_fn_021dbb9c
    cmp r0, #0
    moveq r6, #1
    mov r0, r5
    mov r1, r4
    bl native_fn_022168e8
    cmp r0, #0
    moveq r6, #1
    cmp r6, #0
    ldreq r0, =0x0223989c
    moveq r1, #100
    streqb r1, [r0, #0x17]
ov001_021f2230_Lac:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x17]
    cmp r1, #100
    movne r0, #0
    ldmneia sp!, {r4, r5, r6, pc}
    mov r1, #0
    strb r1, [r0, #0x17]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
