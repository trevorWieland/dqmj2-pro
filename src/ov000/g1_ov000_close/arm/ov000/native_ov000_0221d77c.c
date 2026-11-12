/* ov000 row 0x0221d77c: 168 bytes.
 *
 * What it does: 40 instructions; 7 call(s) to 0x0206d9c8, 0x0206c88c, 0x0206ccb4, +4 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x02246340 (image word 0x02246340)
 *   pool +0xa4 -> constant 0x02246318 (image word 0x02246318)
 *   branch +0x38 -> +0x88
 *   back edge +0x94 -> +0x28
 *   test +0x30 cmp r0, #0
 *   test +0x90 cmp r7, #5
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221d77c; the literal pool and
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

extern void native_fn_0206d9c8(void);
extern void native_fn_0206c88c(void);
extern void native_fn_0206ccb4(void);
extern void native_fn_0206d114(void);
extern void native_fn_0206cf44(void);
extern void native_fn_0206da10(void);


asm u32 native_ov000_0221d77c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r9, r1
    bl native_fn_0206d9c8
    ldr r8, =0x02246340
    ldr r11, =0x02246318
    mov r7, #0
    mvn r4, #0
    mov r6, #2
    mov r5, #12
ov000_0221d77c_L28:
    mov r0, r7, lsl #1
    ldrsh r0, [r10, r0]
    cmp r0, #0
    streqb r4, [r8]
    beq ov000_0221d77c_L88
    str r6, [sp]
    ldrb r1, [r9, r7]
    mov r2, #1
    mov r3, #32
    bl native_fn_0206c88c
    strb r0, [r8]
    str r5, [sp]
    ldrsb r1, [r8]
    ldr r0, [r11, #0x10]
    mov r2, #3
    mov r3, #0
    bl native_fn_0206ccb4
    ldrsb r0, [r8]
    mov r1, #0
    bl native_fn_0206d114
    ldrsb r0, [r8]
    mov r1, #192
    mov r2, #40
    bl native_fn_0206cf44
ov000_0221d77c_L88:
    add r8, r8, #1
    add r7, r7, #1
    cmp r7, #5
    blt ov000_0221d77c_L28
    bl native_fn_0206da10
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
