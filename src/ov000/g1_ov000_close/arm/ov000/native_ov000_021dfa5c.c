/* ov000 row 0x021dfa5c: 160 bytes.
 *
 * What it does: 37 instructions; 4 call(s) to 0x0201d800, 0x021dfa80, 0x0201d800, +1 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x94 -> constant 0x02231bf0 (image word 0x02231bf0)
 *   pool +0x98 -> constant 0x00000136 (image word 0x00000136)
 *   pool +0x9c -> constant 0x02231f64 (image word 0x02231f64)
 *   branch +0x1c -> +0x50
 *   branch +0x38 -> +0x8c
 *   back edge +0x48 -> +0x24
 *   branch +0x4c -> +0x8c
 *   branch +0x64 -> +0x7c
 *   branch +0x78 -> +0x8c
 *   back edge +0x88 -> +0x54
 *   test +0x14 cmp r8, #0
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r6, r5
 *   test +0x60 cmp r0, #0
 *   test +0x80 cmp r6, #16
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dfa5c; the literal pool and
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

extern void native_fn_0201d800(void);


asm u32 native_ov000_021dfa5c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r1, =0x02231bf0
    mov r4, r0
    ldr r8, [r1, #0x8]
    mvn r7, #0
    cmp r8, #0
    mov r6, #0
    beq ov000_021dfa5c_L50
    ldr r5, =0x00000136
ov000_021dfa5c_L24:
    mov r0, r8
    mov r1, r4
    bl native_fn_0201d800
    cmp r0, #0
    moveq r7, r6
    beq ov000_021dfa5c_L8c
    add r6, r6, #1
    cmp r6, r5
    add r8, r8, #44
    blt ov000_021dfa5c_L24
    b ov000_021dfa5c_L8c
ov000_021dfa5c_L50:
    ldr r5, =0x02231f64
ov000_021dfa5c_L54:
    mov r1, r4
    add r0, r5, #4
    bl native_fn_0201d800
    cmp r0, #0
    bne ov000_021dfa5c_L7c
    mov r0, #48
    mul r1, r6, r0
    ldr r0, =0x02231f64
    ldr r7, [r0, r1]
    b ov000_021dfa5c_L8c
ov000_021dfa5c_L7c:
    add r6, r6, #1
    cmp r6, #16
    add r5, r5, #48
    blt ov000_021dfa5c_L54
ov000_021dfa5c_L8c:
    mov r0, r7
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
