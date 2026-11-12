/* ov001 row 0x022020d8: 48 bytes.
 *
 * What it does: 11 instructions; 2 call(s) to 0x02041814, 0x021fe74c; loops (back edge at +0x04); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (11 instructions, 2 calls, 0 branches, 2 back edges, 1 literal slot).
 *
 *   pool +0x2c -> constant 0x02239c10 (image word 0x02239c10)
 *   test +0x08 cmp r0, #1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022020d8; the literal pool and
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

extern void native_fn_02041814(void);
extern void native_fn_021fe74c(void);


asm u32 native_ov001_022020d8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02041814
    cmp r0, #1
    mov r0, #0
    ldmeqia sp!, {r3, pc}
    bl native_fn_021fe74c
    ldr r0, =0x02239c10
    mov r1, #25
    strb r1, [r0, #0xa]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
