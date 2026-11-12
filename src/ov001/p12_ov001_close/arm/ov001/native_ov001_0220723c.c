/* ov001 row 0x0220723c: 64 bytes.
 *
 * What it does: 16 instructions; 2 call(s) to 0x022068a0, 0x02207250; loops (back edge at +0x08); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 2 calls (16 instructions, 2 calls, 1 branch, 2 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x38
 *   back edge +0x34 -> +0x14
 *   test +0x1c cmp r4, r1
 *   test +0x30 cmp r3, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220723c; the literal pool and
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

extern void native_fn_022068a0(void);


asm u32 native_ov001_0220723c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    bl native_fn_022068a0
    mvn r2, #0
    mov r3, #0
ov001_0220723c_L14:
    add r1, r0, r3, lsl #2
    ldr r1, [r1, #0x84]
    cmp r4, r1
    moveq r2, r3
    beq ov001_0220723c_L38
    add r1, r3, #1
    and r3, r1, #255
    cmp r3, #3
    blo ov001_0220723c_L14
ov001_0220723c_L38:
    mov r0, r2
    ldmia sp!, {r4, pc}
}
