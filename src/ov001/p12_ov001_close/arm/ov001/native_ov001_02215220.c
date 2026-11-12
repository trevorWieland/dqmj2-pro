/* ov001 row 0x02215220: 84 bytes.
 *
 * What it does: 18 instructions; 1 call(s) to 0x02215234; loops (back edge at +0x28); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (18 instructions, 2 calls, 1 branch, 1 back edge, 3 literal slots).
 *
 *   pool +0x48 -> constant 0x02242b94 (image word 0x02242b94)
 *   pool +0x4c -> native_data_0222f1cc (image word 0x0222f1cc)
 *   pool +0x50 -> native_data_0222f1d0 (image word 0x0222f1d0)
 *   branch +0x1c -> +0x2c
 *   back edge +0x28 -> +0x14
 *   test +0x18 cmp r3, r0
 *   test +0x24 cmp r2, #5
 *   test +0x2c cmp r2, #5
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02215220; the literal pool and
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

extern u8 native_data_0222f1cc[];
extern u8 native_data_0222f1d0[];


asm u32 native_ov001_02215220 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02242b94
    ldr r1, =native_data_0222f1cc
    ldrh r3, [r0, #4]
    mov r2, #0
ov001_02215220_L14:
    ldrb r0, [r1, r2, lsl #3]
    cmp r3, r0
    beq ov001_02215220_L2c
    add r2, r2, #1
    cmp r2, #5
    blt ov001_02215220_L14
ov001_02215220_L2c:
    cmp r2, #5
    movge r0, #1
    ldmgeia sp!, {r3, pc}
    ldr r0, =native_data_0222f1d0
    ldr r0, [r0, r2, lsl #3]
    blx r0
    ldmia sp!, {r3, pc}
}
