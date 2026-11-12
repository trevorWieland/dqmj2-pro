/* ov001 row 0x021feb50: 84 bytes.
 *
 * What it does: 20 instructions; 2 call(s) to 0x0202a498, 0x0202a498; loops (back edge at +0x18); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (20 instructions, 2 calls, 1 branch, 2 back edges, 1 literal slot).
 *
 *   pool +0x50 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x10 -> +0x28
 *   test +0x0c cmp r1, #0
 *   test +0x30 cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021feb50; the literal pool and
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

extern void native_fn_0202a498(void);


asm u32 native_ov001_021feb50 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02239c10
    ldr r1, [r0, #0x44]
    cmp r1, #0
    beq ov001_021feb50_L28
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x02239c10
    mov r1, #0
    str r1, [r0, #0x44]
ov001_021feb50_L28:
    ldr r0, =0x02239c10
    ldr r1, [r0, #0x48]
    cmp r1, #0
    ldmeqia sp!, {r3, pc}
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x02239c10
    mov r1, #0
    str r1, [r0, #0x48]
    ldmia sp!, {r3, pc}
}
