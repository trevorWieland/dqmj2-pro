/* ov001 row 0x0220795c: 72 bytes.
 *
 * What it does: 18 instructions; 2 call(s) to 0x02207938, 0x02207974; loops (back edge at +0x04); returns through pop {r3, pc}
 *
 * Decoded shape: loop with 2 calls (18 instructions, 2 calls, 0 branches, 2 back edges, 0 literal slots).
 *
 *   back edge +0x40 -> +0x18
 *   test +0x20 cmp r1, #0
 *   test +0x3c cmp r2, #64
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220795c; the literal pool and
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

extern void native_fn_02207938(void);


asm u32 native_ov001_0220795c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02207938
    ldr r3, [r0, #0x10]
    mov r1, #0
    str r1, [r0, #0x544]
    mov r2, #2
ov001_0220795c_L18:
    add r1, r3, r2
    ldrb r1, [r1, #0x35e]
    cmp r1, #0
    ldrne r1, [r0, #0x544]
    addne r1, r1, #1
    strne r1, [r0, #0x544]
    add r1, r2, #1
    mov r1, r1, lsl #24
    mov r2, r1, asr #24
    cmp r2, #64
    blt ov001_0220795c_L18
    ldmia sp!, {r3, pc}
}
