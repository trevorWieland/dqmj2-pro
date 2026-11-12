/* ov000 row 0x02227980: 212 bytes.
 *
 * What it does: 51 instructions; 7 call(s) to 0x022256e4, 0x02008e0c, 0x02227994, +4 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xcc -> constant 0x02246aa8 (image word 0x02246aa8)
 *   pool +0xd0 -> constant 0x022468e0 (image word 0x022468e0)
 *   branch +0x28 -> +0x64
 *   branch +0x60 -> +0x78
 *   back edge +0x74 -> +0x14
 *   branch +0x7c -> +0xc4
 *   back edge +0xbc -> +0x88
 *   test +0x24 cmp r0, #0
 *   test +0x3c cmp r1, #64
 *   test +0x70 cmp r7, #14
 *   test +0x78 cmp r6, #0
 *   test +0xb0 cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02227980; the literal pool and
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
extern void native_fn_020d1810(void);
extern void native_fn_02227e80(void);
extern void native_fn_02227cec(void);


asm u32 native_ov000_02227980 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, #0
    ldr r5, =0x02246aa8
    mov r4, r6
    mov r7, r6
ov000_02227980_L14:
    add r0, r7, #48
    mov r0, r0, lsl #16
    mov r0, r0, lsr #16
    bl native_fn_022256e4
    cmp r0, #0
    beq ov000_02227980_L64
    rsb r7, r7, r7, lsl #6
    ldrb r6, [r0]
    rsb r1, r7, #152
    mov r2, #64
    cmp r1, #64
    movlo r2, r1
    ldr r3, =0x022468e0
    mov r1, #152
    mla r1, r6, r1, r3
    add r0, r0, #1
    add r1, r1, r7
    bl native_fn_02008e0c
    mov r6, #1
    b ov000_02227980_L78
ov000_02227980_L64:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #14
    blt ov000_02227980_L14
ov000_02227980_L78:
    cmp r6, #0
    bne ov000_02227980_Lc4
    ldr r4, =0x022468e0
    mov r6, #0
ov000_02227980_L88:
    mov r0, r4
    mov r1, r5
    bl native_fn_020d1810
    mov r0, r5
    bl native_fn_02227e80
    mov r0, r5
    bl native_fn_02227cec
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #3
    add r5, r5, #132
    add r4, r4, #152
    blt ov000_02227980_L88
    mov r4, #1
ov000_02227980_Lc4:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
