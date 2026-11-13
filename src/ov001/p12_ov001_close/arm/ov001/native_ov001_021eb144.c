/* ov001 row 0x021eb144: 188 bytes.
 *
 * What it does: 46 instructions; 3 call(s) to 0x021db438, 0x021db438, 0x02008d78; loops (back edge at +0x48); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (46 instructions, 3 calls, 3 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0xb8 -> constant 0x02238d7c (image word 0x02238d7c)
 *   branch +0x18 -> +0x68
 *   branch +0x28 -> +0x58
 *   branch +0x54 -> +0x68
 *   test +0x10 cmp r1, #0
 *   test +0x24 cmp r0, r1
 *   test +0x2c cmp r1, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eb144; the literal pool and
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
extern void native_fn_02008d78(void);


asm u32 native_ov001_021eb144 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x02238d7c
    ldr r1, [r0, #0x54]
    ldr r4, [r0, #0x60]
    cmp r1, #0
    strne r1, [r0, #0x60]
    bne ov001_021eb144_L68
    ldrb r1, [r4, #0x31e]
    ldrb r0, [r0, #0x24]
    cmp r0, r1
    beq ov001_021eb144_L58
    cmp r1, #0
    moveq r3, #1
    movne r3, #0
    ldr r2, =0x02238d7c
    and r0, r3, #255
    mov r1, #0
    strb r3, [r2, #0x24]
    bl ov001_side_slot_record_021db438
    ldr r1, =0x02238d7c
    str r0, [r1, #0x60]
    b ov001_021eb144_L68
ov001_021eb144_L58:
    mov r1, #0
    bl ov001_side_slot_record_021db438
    ldr r1, =0x02238d7c
    str r0, [r1, #0x60]
ov001_021eb144_L68:
    ldr r0, =0x02238d7c
    mov r1, #0
    str r4, [r0, #0x54]
    ldr r0, [r0, #0x60]
    mov r2, #6
    add r0, r0, #78
    add r0, r0, #768
    bl native_fn_02008d78
    ldr r1, =0x02238d7c
    mov r3, #0
    ldr r0, [r1, #0x54]
    sub r2, r3, #1
    strb r3, [r0, #0x357]
    ldr r0, [r1, #0x54]
    add r0, r0, #768
    strh r2, [r0, #64]
    ldr r0, [r1, #0x54]
    add r0, r0, #768
    strh r2, [r0, #66]
    ldmia sp!, {r4, pc}
}
