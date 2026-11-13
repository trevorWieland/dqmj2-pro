/* ov001 row 0x021f42b8: 132 bytes.
 *
 * What it does: 32 instructions; 4 call(s) to 0x021db438, 0x021db8d0, 0x021dc5d4, +1 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (32 instructions, 4 calls, 3 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x80 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x08 -> +0x38
 *   branch +0x34 -> +0x3c
 *   branch +0x58 -> +0x6c
 *   back edge +0x78 -> +0x4c
 *   test +0x1c cmp r0, #0
 *   test +0x40 cmp r5, #0
 *   test +0x54 cmp r0, #0
 *   test +0x70 cmp r6, r5
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f42b8; the literal pool and
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
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dc5d4(void);


asm u32 native_ov001_021f42b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    movs r7, r0
    bne ov001_021f42b8_L38
    ldr r0, =0x0223989c
    mov r1, #0
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    bl ov001_side_slot_record_021db438
    mov r7, r0
    mov r5, #3
    b ov001_021f42b8_L3c
ov001_021f42b8_L38:
    mov r5, #1
ov001_021f42b8_L3c:
    mov r6, #0
    cmp r5, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, pc}
    mov r4, r6
ov001_021f42b8_L4c:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f42b8_L6c
    mov r0, r7
    bl native_fn_021dc5d4
    add r0, r7, #768
    strh r4, [r0, #76]
ov001_021f42b8_L6c:
    add r6, r6, #1
    cmp r6, r5
    add r7, r7, #1088
    blt ov001_021f42b8_L4c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
