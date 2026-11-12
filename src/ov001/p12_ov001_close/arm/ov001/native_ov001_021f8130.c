/* ov001 row 0x021f8130: 216 bytes.
 *
 * What it does: 53 instructions; 3 call(s) to 0x021dbf98, 0x021ee91c, 0x021dbf98; loops (back edge at +0x34); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (53 instructions, 3 calls, 5 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0xd4 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x10 -> +0x8c
 *   branch +0x88 -> +0xcc
 *   branch +0x90 -> +0xb4
 *   branch +0xb0 -> +0xcc
 *   branch +0xb8 -> +0xcc
 *   test +0x0c cmp r0, #0
 *   test +0x8c cmp r0, #30
 *   test +0xa4 cmp r0, #30
 *   test +0xb4 cmp r0, #100
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f8130; the literal pool and
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

extern void native_fn_021dbf98(void);
extern void native_fn_021ee91c(void);


asm u32 native_ov001_021f8130 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r3, =0x0223989c
    ldrsb r0, [r3, #42]
    cmp r0, #0
    bne ov001_021f8130_L8c
    mov r0, #1
    str r0, [sp]
    ldr r0, [r3, #0x84]
    mov r1, #8
    add r0, r0, #512
    ldrsb r2, [r0, #52]
    ldr r0, [r3, #0x80]
    sub r3, r1, #9
    bl native_fn_021dbf98
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    add r1, r0, #512
    ldrsb r1, [r1, #52]
    bl native_fn_021ee91c
    ldr r0, =0x0223989c
    mov r1, #8
    ldr r0, [r0, #0x84]
    mov r2, #1
    str r2, [sp]
    add r2, r0, #512
    ldrsb r2, [r2, #52]
    sub r3, r1, #9
    rsb r2, r2, #0
    bl native_fn_021dbf98
    ldr r0, =0x0223989c
    mov r1, #30
    strb r1, [r0, #0x2a]
    mov r1, #0
    strb r1, [r0, #0x1c]
    b ov001_021f8130_Lcc
ov001_021f8130_L8c:
    cmp r0, #30
    bne ov001_021f8130_Lb4
    ldrsb r0, [r3, #28]
    add r0, r0, #1
    strb r0, [r3, #0x1c]
    ldrsb r0, [r3, #28]
    cmp r0, #30
    movgt r0, #100
    strgtb r0, [r3, #0x2a]
    b ov001_021f8130_Lcc
ov001_021f8130_Lb4:
    cmp r0, #100
    bne ov001_021f8130_Lcc
    mov r0, #0
    strb r0, [r3, #0x2a]
    mov r0, #27
    strb r0, [r3, #0x1b]
ov001_021f8130_Lcc:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
