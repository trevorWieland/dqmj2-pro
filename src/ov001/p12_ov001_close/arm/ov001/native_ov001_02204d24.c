/* ov001 row 0x02204d24: 60 bytes.
 *
 * What it does: 15 instructions; 3 call(s) to 0x02204250, 0x022042c4, 0x02204d30; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 3 calls (15 instructions, 3 calls, 1 branch, 3 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x24
 *   back edge +0x34 -> +0x0c
 *   test +0x18 cmp r1, r5
 *   test +0x30 cmp r4, #64
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204d24; the literal pool and
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

extern void native_fn_02204250(void);
extern void native_fn_022042c4(void);


asm u32 native_ov001_02204d24 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #0
ov001_02204d24_Lc:
    mov r0, r4
    bl native_fn_02204250
    ldr r1, [r0]
    cmp r1, r5
    bne ov001_02204d24_L24
    bl native_fn_022042c4
ov001_02204d24_L24:
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #64
    blt ov001_02204d24_Lc
    ldmia sp!, {r3, r4, r5, pc}
}
