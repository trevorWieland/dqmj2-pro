/* ov000 row 0x02223118: 120 bytes.
 *
 * What it does: 28 instructions; 4 call(s) to 0x0201d444, 0x02223390, 0x0205e7a8, +1 more; loops (back edge at +0x30); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x02246574 (image word 0x02246574)
 *   pool +0x74 -> native_data_0222fd4c (image word 0x0222fd4c)
 *   branch +0x1c -> +0x64
 *   test +0x18 tst r0, #255
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02223118; the literal pool and
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

extern u8 native_data_0222fd4c[];
extern void native_fn_0201d444(void);
extern void native_fn_02223390(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_0205e814(void);


asm u32 native_ov000_02223118 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #32
    ldr r2, =0x02246574
    ldrb r0, [r2, #0x1]
    sub r0, r0, #1
    strb r0, [r2, #0x1]
    tst r0, #255
    bne ov000_02223118_L64
    ldr r1, =native_data_0222fd4c
    mov r3, #10
    add r0, sp, #0
    strb r3, [r2]
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_02223390
    mvn r0, #0
    mov r1, #147
    bl native_fn_0205e7a8
    mov r0, #0
    mov r1, r0
    mov r2, #30
    bl native_fn_0205e814
    ldr r0, =0x02246574
    mov r1, #40
    strb r1, [r0, #0x1]
ov000_02223118_L64:
    mov r0, #0
    add sp, sp, #32
    ldmia sp!, {r3, pc}
}
