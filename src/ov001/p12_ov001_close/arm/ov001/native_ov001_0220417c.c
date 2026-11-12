/* ov001 row 0x0220417c: 172 bytes.
 *
 * What it does: 40 instructions; 1 call(s) to 0x022042c4; no back edge; returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: branched body (40 instructions, 4 calls, 3 branches, 0 back edges, 3 literal slots).
 *
 *   pool +0xa0 -> native_data_0222e068 (image word 0x0222e068)
 *   pool +0xa4 -> native_data_0222e06c (image word 0x0222e06c)
 *   pool +0xa8 -> native_data_0222e070 (image word 0x0222e070)
 *   branch +0x1c -> +0x34
 *   branch +0x24 -> +0x54
 *   branch +0x2c -> +0x98
 *   test +0x0c cmp r3, #127
 *   test +0x18 cmp r1, #0
 *   test +0x20 cmp r1, #1
 *   test +0x28 cmp r1, #2
 *   test +0x68 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220417c; the literal pool and
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

extern u8 native_data_0222e068[];
extern u8 native_data_0222e06c[];
extern u8 native_data_0222e070[];
extern void native_fn_022042c4(void);


asm u32 native_ov001_0220417c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldr r3, [r4]
    cmp r3, #127
    ldmeqia sp!, {r4, pc}
    ldr r1, [r4, #0x4]
    cmp r1, #0
    beq ov001_0220417c_L34
    cmp r1, #1
    beq ov001_0220417c_L54
    cmp r1, #2
    beq ov001_0220417c_L98
    ldmia sp!, {r4, pc}
ov001_0220417c_L34:
    mov r1, #12
    mul r2, r3, r1
    ldr r1, =native_data_0222e068
    ldr r1, [r1, r2]
    blx r1
    mov r0, #1
    str r0, [r4, #0x4]
    ldmia sp!, {r4, pc}
ov001_0220417c_L54:
    mov r1, #12
    mul r2, r3, r1
    ldr r1, =native_data_0222e06c
    ldr r1, [r1, r2]
    blx r1
    cmp r0, #0
    ldmeqia sp!, {r4, pc}
    ldr r1, [r4]
    mov r0, #12
    mul r2, r1, r0
    ldr r1, =native_data_0222e070
    mov r0, r4
    ldr r1, [r1, r2]
    blx r1
    mov r0, #2
    str r0, [r4, #0x4]
    ldmia sp!, {r4, pc}
ov001_0220417c_L98:
    bl native_fn_022042c4
    ldmia sp!, {r4, pc}
}
