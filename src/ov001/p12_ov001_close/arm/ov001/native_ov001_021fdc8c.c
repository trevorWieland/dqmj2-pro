/* ov001 row 0x021fdc8c: 104 bytes.
 *
 * What it does: 24 instructions; 2 call(s) to 0x021db530, 0x021fdcf4; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (24 instructions, 2 calls, 2 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x60 -> native_data_0222edc8 (image word 0x0222edc8)
 *   pool +0x64 -> native_data_0222edcc (image word 0x0222edcc)
 *   branch +0x2c -> +0x40
 *   back edge +0x58 -> +0x24
 *   test +0x14 cmp r4, #0
 *   test +0x28 cmp r0, #127
 *   test +0x48 cmp r4, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fdc8c; the literal pool and
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

extern void ov001_mode_byte_021db530(void);
extern u8 native_data_0222edc8[];
extern u8 native_data_0222edcc[];
extern void native_fn_021fdcf4(void);


asm u32 native_ov001_021fdc8c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r0, #0
    bl ov001_mode_byte_021db530
    mov r4, r0
    mov r5, #0
    cmp r4, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r6, =native_data_0222edc8
    ldr r7, =native_data_0222edcc
ov001_021fdc8c_L24:
    ldrsb r0, [r6]
    cmp r0, #127
    bne ov001_021fdc8c_L40
    ldrb r2, [r7]
    mov r0, r5
    mov r1, r4
    bl native_fn_021fdcf4
ov001_021fdc8c_L40:
    add r0, r5, #1
    mov r0, r0, lsl #24
    cmp r4, r0, asr #24
    add r6, r6, #1
    add r7, r7, #1
    mov r5, r0, asr #24
    bgt ov001_021fdc8c_L24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
