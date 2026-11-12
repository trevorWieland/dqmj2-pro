/* ov000 row 0x021f8bb8: 104 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x0203d350, 0x0205f98c, 0x0204b178; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x02236f2c (image word 0x02236f2c)
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmp r4, #0
 *   test +0x54 cmp r1, #2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8bb8; the literal pool and
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

extern void native_fn_0203d350(void);
extern void native_fn_0205f98c(void);
extern void native_fn_0204b178(void);


asm u32 native_ov000_021f8bb8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r5, =0x02236f2c
    bl native_fn_0203d350
    mov r1, r5
    mov r4, r0
    ldr r0, [r1, #0x1c]
    cmp r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
    ldr r0, [r5, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    cmp r4, #0
    movne r1, #19
    mov r6, r0
    moveq r1, #20
    str r4, [r5, #0x2c]
    mov r0, r6
    and r1, r1, #255
    bl native_fn_0204b178
    ldr r0, [r6, #0x7c]
    and r1, r0, #2
    cmp r1, #2
    orrne r0, r0, #2
    strne r0, [r6, #0x7c]
    ldmia sp!, {r4, r5, r6, pc}
}
