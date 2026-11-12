/* ov001 row 0x02213c78: 108 bytes.
 *
 * What it does: 26 instructions; 5 call(s) to 0x021db438, 0x021db530, 0x02213cd8, +2 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (26 instructions, 5 calls, 0 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0x68 -> constant 0x02242aac (image word 0x02242aac)
 *   branch +0x44 -> +0x60
 *   back edge +0x5c -> +0x48
 *   test +0x18 cmp r0, #0
 *   test +0x3c cmp r5, #0
 *   test +0x54 cmp r6, r5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213c78; the literal pool and
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
extern void ov001_mode_byte_021db530(void);
extern void ov001_record_is_active_021db8d0(void);


asm u32 native_ov001_02213c78 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x02242aac
    mov r1, #0
    ldr r0, [r0, #0x4]
    mov r4, r2
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r5, #1
    movne r5, #0
    mov r0, r5
    bl ov001_side_slot_record_021db438
    mov r7, r0
    mov r0, r5
    bl ov001_mode_byte_021db530
    mov r5, r0
    cmp r5, #0
    mov r6, #0
    ble ov001_02213c78_L60
ov001_02213c78_L48:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    add r6, r6, #1
    cmp r6, r5
    add r7, r7, #1088
    blt ov001_02213c78_L48
ov001_02213c78_L60:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
