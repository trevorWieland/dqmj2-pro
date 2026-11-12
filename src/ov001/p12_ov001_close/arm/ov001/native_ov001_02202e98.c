/* ov001 row 0x02202e98: 140 bytes.
 *
 * What it does: 33 instructions; 4 call(s) to 0x022027c0, 0x022027f0, 0x02204250, +1 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, r8, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (33 instructions, 4 calls, 3 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0x84 -> native_data_0222edc8 (image word 0x0222edc8)
 *   pool +0x88 -> constant 0x0223a030 (image word 0x0223a030)
 *   branch +0x20 -> +0x68
 *   branch +0x3c -> +0x4c
 *   branch +0x48 -> +0x58
 *   back edge +0x7c -> +0x18
 *   test +0x1c cmp r0, #127
 *   test +0x38 cmp r2, #14
 *   test +0x74 cmp r7, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202e98; the literal pool and
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

extern u8 native_data_0222edc8[];
extern void native_fn_022027c0(void);
extern void native_fn_022027f0(void);
extern void native_fn_02204250(void);


asm u32 native_ov001_02202e98 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r5, #1
    ldr r8, =native_data_0222edc8
    ldr r6, =0x0223a030
    mov r7, #0
    mov r4, r5
ov001_02202e98_L18:
    ldrsb r0, [r8]
    cmp r0, #127
    beq ov001_02202e98_L68
    add r1, r6, r7, lsl #3
    add r0, r1, #512
    ldrsb r2, [r0, #24]
    ldrsb r3, [r0, #25]
    ldr r0, [r1, #0x214]
    cmp r2, #14
    beq ov001_02202e98_L4c
    mov r1, r7
    bl native_fn_022027c0
    b ov001_02202e98_L58
ov001_02202e98_L4c:
    mov r1, r7
    mov r2, r5
    bl native_fn_022027f0
ov001_02202e98_L58:
    strb r0, [r8]
    ldrsb r0, [r8]
    bl native_fn_02204250
    str r4, [r0, #0x38]
ov001_02202e98_L68:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #3
    add r8, r8, #1
    blt ov001_02202e98_L18
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
