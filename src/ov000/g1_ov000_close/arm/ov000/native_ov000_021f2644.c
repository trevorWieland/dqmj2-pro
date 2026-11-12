/* ov000 row 0x021f2644: 112 bytes.
 *
 * What it does: 27 instructions; 2 call(s) to 0x02062b9c, 0x021f2654; loops (back edge at +0x30); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x6c -> constant 0x02236d98 (image word 0x02236d98)
 *   branch +0x2c -> +0x5c
 *   branch +0x38 -> +0x5c
 *   back edge +0x64 -> +0x10
 *   test +0x28 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x60 cmp r5, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f2644; the literal pool and
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

extern void native_fn_02062b9c(void);


asm u32 native_ov000_021f2644 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, #0
    ldr r6, =0x02236d98
    mov r4, r5
ov000_021f2644_L10:
    ldr r0, [r6, #0x8]
    add r1, r0, r5, lsl #2
    add r0, r1, #6400
    ldrsh r0, [r0, #12]
    add r1, r1, #4096
    ldrb r1, [r1, #0x90e]
    cmp r0, #0
    beq ov000_021f2644_L5c
    bl native_fn_02062b9c
    cmp r0, #0
    bne ov000_021f2644_L5c
    ldr r0, [r6, #0x8]
    add r0, r0, r5, lsl #2
    add r0, r0, #6400
    strh r4, [r0, #12]
    ldr r0, [r6, #0x8]
    add r0, r0, r5, lsl #2
    add r0, r0, #4096
    strb r4, [r0, #0x90e]
ov000_021f2644_L5c:
    add r5, r5, #1
    cmp r5, #3
    blt ov000_021f2644_L10
    ldmia sp!, {r4, r5, r6, pc}
}
