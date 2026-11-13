/* ov001 row 0x021f4210: 168 bytes.
 *
 * What it does: 41 instructions; 2 call(s) to 0x021db438, 0x021db438; loops (back edge at +0x54); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (41 instructions, 2 calls, 4 branches, 2 back edges, 1 literal slot).
 *
 *   pool +0xa4 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x14 -> +0x28
 *   branch +0x24 -> +0x74
 *   branch +0x34 -> +0x64
 *   branch +0x60 -> +0x74
 *   test +0x10 cmp r1, #0
 *   test +0x30 cmp r0, r1
 *   test +0x38 cmp r1, #0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f4210; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);


asm u32 native_ov001_021f4210 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x0223989c
    ldr r1, [r0, #0x80]
    ldr r4, [r0, #0x84]
    cmp r1, #0
    beq ov001_021f4210_L28
    str r1, [r0, #0x84]
    ldrb r1, [r1, #0x31e]
    strb r1, [r0, #0x11]
    b ov001_021f4210_L74
ov001_021f4210_L28:
    ldrb r1, [r4, #0x31e]
    ldrb r0, [r0, #0x11]
    cmp r0, r1
    beq ov001_021f4210_L64
    cmp r1, #0
    moveq r3, #1
    movne r3, #0
    ldr r2, =0x0223989c
    and r0, r3, #255
    mov r1, #0
    strb r3, [r2, #0x11]
    bl ov001_side_slot_record_021db438
    ldr r1, =0x0223989c
    str r0, [r1, #0x84]
    b ov001_021f4210_L74
ov001_021f4210_L64:
    mov r1, #0
    bl ov001_side_slot_record_021db438
    ldr r1, =0x0223989c
    str r0, [r1, #0x84]
ov001_021f4210_L74:
    ldr r1, =0x0223989c
    mov r2, #0
    str r4, [r1, #0x80]
    strb r2, [r4, #0x357]
    ldr r0, [r1, #0x80]
    sub r2, r2, #1
    add r0, r0, #768
    strh r2, [r0, #64]
    ldr r0, [r1, #0x80]
    add r0, r0, #768
    strh r2, [r0, #66]
    ldmia sp!, {r4, pc}
}
