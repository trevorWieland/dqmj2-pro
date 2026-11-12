/* ov001 row 0x02211918: 168 bytes.
 *
 * What it does: 40 instructions; 1 call(s) to 0x0201af84; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (40 instructions, 1 call, 3 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0xa0 -> native_data_0222e10c (image word 0x0222e10c)
 *   pool +0xa4 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x28 -> +0x8c
 *   branch +0x3c -> +0x8c
 *   back edge +0x88 -> +0x4c
 *   test +0x2c cmp r8, #0
 *   test +0x38 cmp r8, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02211918; the literal pool and
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

extern u8 native_data_0222e10c[];
extern void native_fn_0201af84(void);


asm u32 native_ov001_02211918 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldrsh r1, [r0, #20]
    ldr r0, [r0, #0x2c]
    mov r9, #0
    mov r0, r0, lsl #16
    add r1, r1, #8
    movs r8, r0, asr #16
    addeq r0, r9, #13
    and r7, r1, #255
    andeq r9, r0, #255
    beq ov001_02211918_L8c
    cmp r8, #0
    addlt r0, r9, #9
    andlt r9, r0, #255
    cmp r8, #0
    beq ov001_02211918_L8c
    ldr r6, =native_data_0222e10c
    ldr r5, =0x66666667
    mov r4, #10
ov001_02211918_L4c:
    mov r0, r8
    bl native_fn_0201af84
    mov r1, r0, lsr #31
    smull r2, r3, r5, r0
    add r3, r1, r3, asr #2
    smull r1, r2, r4, r3
    sub r3, r0, r1
    ldrb r2, [r6, r3]
    smull r0, r1, r5, r8
    mov r0, r8, lsr #31
    add r1, r0, r1, asr #2
    add r2, r9, r2
    mov r0, r1, lsl #16
    and r9, r2, #255
    movs r8, r0, asr #16
    bne ov001_02211918_L4c
ov001_02211918_L8c:
    mov r0, r9, asr #1
    and r0, r0, #255
    sub r0, r7, r0
    and r0, r0, #255
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
