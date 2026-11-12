/* ov001 row 0x021e1358: 80 bytes.
 *
 * What it does: 20 instructions; 3 call(s) to 0x021db438, 0x021db8d0, 0x021e1374; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 3 calls (20 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x3c
 *   back edge +0x48 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x40 cmp r6, #3
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e1358; the literal pool and
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


asm u32 native_ov001_021e1358 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r6, #0
    mov r7, r0
    mov r5, r6
    mvn r4, #0
ov001_021e1358_L1c:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021e1358_L3c
    strb r5, [r7, #0x357]
    add r0, r7, #768
    strh r4, [r0, #64]
    strh r4, [r0, #66]
ov001_021e1358_L3c:
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_021e1358_L1c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
