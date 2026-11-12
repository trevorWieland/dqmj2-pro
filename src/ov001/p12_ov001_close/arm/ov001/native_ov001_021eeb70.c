/* ov001 row 0x021eeb70: 124 bytes.
 *
 * What it does: 29 instructions; 2 call(s) to 0x021eeb84, 0x0205c9bc; loops (back edge at +0x30); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (29 instructions, 2 calls, 3 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x74 -> constant 0x02238e58 (image word 0x02238e58)
 *   pool +0x78 -> constant 0x02238e5c (image word 0x02238e5c)
 *   branch +0x24 -> +0x34
 *   back edge +0x30 -> +0x14
 *   branch +0x38 -> +0x6c
 *   branch +0x54 -> +0x6c
 *   test +0x18 cmp r0, r1
 *   test +0x2c cmp r12, #32
 *   test +0x34 cmp lr, #0
 *   test +0x48 tst r1, #255
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eeb70; the literal pool and
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

extern void native_fn_0205c9bc(void);


asm u32 native_ov001_021eeb70 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r3, #0
    ldr r2, =0x02238e58
    mov lr, r3
    mov r12, r3
ov001_021eeb70_L14:
    ldr r1, [r2, r12, lsl #3]
    cmp r0, r1
    moveq r4, r12
    moveq lr, #1
    beq ov001_021eeb70_L34
    add r12, r12, #1
    cmp r12, #32
    blt ov001_021eeb70_L14
ov001_021eeb70_L34:
    cmp lr, #0
    beq ov001_021eeb70_L6c
    ldr r2, =0x02238e5c
    ldrb r1, [r2, r4, lsl #3]
    sub r1, r1, #1
    tst r1, #255
    strb r1, [r2, r4, lsl #3]
    movne r3, #1
    bne ov001_021eeb70_L6c
    bl native_fn_0205c9bc
    ldr r1, =0x02238e58
    mov r2, #0
    mov r3, r0
    str r2, [r1, r4, lsl #3]
ov001_021eeb70_L6c:
    mov r0, r3
    ldmia sp!, {r4, pc}
}
