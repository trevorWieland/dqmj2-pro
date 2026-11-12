/* ov001 row 0x02213630: 104 bytes.
 *
 * What it does: 26 instructions; 4 call(s) to 0x021f1a44, 0x02204250, 0x021f1a44, +1 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 4 calls (26 instructions, 4 calls, 4 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x50
 *   branch +0x30 -> +0x3c
 *   branch +0x38 -> +0x40
 *   branch +0x4c -> +0x60
 *   back edge +0x5c -> +0x1c
 *   test +0x24 cmp r0, #127
 *   test +0x2c cmp r5, #3
 *   test +0x44 cmp r0, #1
 *   test +0x58 cmp r5, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213630; the literal pool and
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

extern void native_fn_021f1a44(void);
extern void native_fn_02204250(void);


asm u32 native_ov001_02213630 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r6, #0
    bl native_fn_021f1a44
    mov r4, r0
    mov r5, r6
ov001_02213630_L1c:
    add r0, r4, r5
    ldrsb r0, [r0, #9]
    cmp r0, #127
    beq ov001_02213630_L50
    cmp r5, #3
    beq ov001_02213630_L3c
    bl native_fn_02204250
    b ov001_02213630_L40
ov001_02213630_L3c:
    bl native_fn_021f1a44
ov001_02213630_L40:
    ldrb r0, [r0, #0x23]
    cmp r0, #1
    moveq r6, #1
    beq ov001_02213630_L60
ov001_02213630_L50:
    add r0, r5, #1
    and r5, r0, #255
    cmp r5, #4
    blo ov001_02213630_L1c
ov001_02213630_L60:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, pc}
}
