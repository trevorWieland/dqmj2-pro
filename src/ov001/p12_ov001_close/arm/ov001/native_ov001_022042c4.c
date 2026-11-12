/* ov001 row 0x022042c4: 76 bytes.
 *
 * What it does: 19 instructions; 3 call(s) to 0x0202a498, 0x0205f920, 0x02204244; loops (back edge at +0x24); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 3 calls (19 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x30
 *   test +0x0c cmp r0, #127
 *   test +0x18 cmp r1, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022042c4; the literal pool and
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
extern void native_fn_0205f920(void);
extern void native_fn_02204244(void);


asm u32 native_ov001_022042c4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldr r0, [r4]
    cmp r0, #127
    ldmeqia sp!, {r4, pc}
    ldr r1, [r4, #0x40]
    cmp r1, #0
    beq ov001_022042c4_L30
    mov r0, #2
    bl native_fn_0202a498
    mov r0, #0
    str r0, [r4, #0x40]
ov001_022042c4_L30:
    mov r0, r4
    mov r1, #1
    mov r2, #2
    bl native_fn_0205f920
    mov r0, r4
    bl native_fn_02204244
    ldmia sp!, {r4, pc}
}
