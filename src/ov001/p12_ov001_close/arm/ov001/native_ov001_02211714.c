/* ov001 row 0x02211714: 72 bytes.
 *
 * What it does: 18 instructions; 3 call(s) to 0x021f1a44, 0x02204250, 0x02211724; loops (back edge at +0x04); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 3 calls (18 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x30
 *   back edge +0x40 -> +0x10
 *   test +0x18 cmp r0, #127
 *   test +0x3c cmp r4, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02211714; the literal pool and
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


asm u32 native_ov001_02211714 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    bl native_fn_021f1a44
    mov r5, r0
    mov r4, #0
ov001_02211714_L10:
    add r0, r5, r4
    ldrsb r0, [r0, #9]
    cmp r0, #127
    beq ov001_02211714_L30
    bl native_fn_02204250
    ldr r1, [r0, #0x44]
    orr r1, r1, #1
    str r1, [r0, #0x44]
ov001_02211714_L30:
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #3
    blt ov001_02211714_L10
    ldmia sp!, {r3, r4, r5, pc}
}
