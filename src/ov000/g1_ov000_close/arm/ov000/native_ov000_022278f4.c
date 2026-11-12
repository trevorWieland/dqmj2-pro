/* ov000 row 0x022278f4: 140 bytes.
 *
 * What it does: 34 instructions; 3 call(s) to 0x022256e4, 0x02008e0c, 0x02227908; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x02246aa8 (image word 0x02246aa8)
 *   branch +0x28 -> +0x64
 *   branch +0x60 -> +0x78
 *   back edge +0x74 -> +0x14
 *   test +0x24 cmp r0, #0
 *   test +0x40 cmp r1, #68
 *   test +0x70 cmp r7, #14
 *   test +0x78 cmp r6, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022278f4; the literal pool and
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

extern void native_fn_022256e4(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov000_022278f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, #0
    ldr r4, =0x02246aa8
    mov r5, r6
    mov r7, r6
ov000_022278f4_L14:
    add r0, r7, #48
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_022256e4
    cmp r0, #0
    beq ov000_022278f4_L64
    mov r1, #67
    mul r6, r7, r1
    ldrb r3, [r0]
    rsb r1, r6, #132
    mov r2, #68
    cmp r1, #68
    movlo r2, r1
    mov r1, #132
    mla r1, r3, r1, r4
    add r0, r0, #1
    add r1, r1, r6
    bl native_fn_02008e0c
    mov r6, #1
    b ov000_022278f4_L78
ov000_022278f4_L64:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #14
    blt ov000_022278f4_L14
ov000_022278f4_L78:
    cmp r6, #0
    moveq r5, #1
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
