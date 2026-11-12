/* ov001 row 0x02219d8c: 76 bytes.
 *
 * What it does: 19 instructions; 2 call(s) to 0x021db8d0, 0x02219d98; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: block load (19 instructions, 2 calls, 1 branch, 2 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x44
 *   back edge +0x40 -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmpne r1, r0
 *   test +0x28 cmp r5, #2
 *   test +0x38 cmp r5, #3
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219d8c; the literal pool and
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

extern void native_fn_021db8d0(void);


asm u32 native_ov001_02219d8c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldmia r0, {r4, r6}
    mov r5, #0
ov001_02219d8c_Lc:
    mov r0, r6
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r1, [r4, #0x31f]
    ldrneb r0, [r6, #0x31f]
    cmpne r1, r0
    bne ov001_02219d8c_L44
    cmp r5, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r5, r5, #1
    cmp r5, #3
    add r6, r6, #1088
    blt ov001_02219d8c_Lc
ov001_02219d8c_L44:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
