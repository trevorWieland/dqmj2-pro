/* ov001 row 0x021f358c: 100 bytes.
 *
 * What it does: 24 instructions; 3 call(s) to 0x021db438, 0x021db8d0, 0x021f35ac; loops (back edge at +0x28); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (24 instructions, 3 calls, 0 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x60 -> constant 0x0223989c (image word 0x0223989c)
 *   back edge +0x54 -> +0x20
 *   test +0x14 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmpne r0, #0
 *   test +0x50 cmp r5, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f358c; the literal pool and
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


asm u32 native_ov001_021f358c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r0, =0x0223989c
    mov r5, #0
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r6, #1
    movne r6, #0
ov001_021f358c_L20:
    mov r0, r6
    mov r1, r5
    bl ov001_side_slot_record_021db438
    mov r4, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    addne r0, r4, #512
    ldrnesb r0, [r0, #103]
    cmpne r0, #0
    movne r0, #1
    ldmneia sp!, {r4, r5, r6, pc}
    add r5, r5, #1
    cmp r5, #3
    blt ov001_021f358c_L20
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
