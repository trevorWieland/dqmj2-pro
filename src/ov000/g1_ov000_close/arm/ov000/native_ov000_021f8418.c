/* ov000 row 0x021f8418: 136 bytes.
 *
 * What it does: 33 instructions; 7 call(s) to 0x0201d444, 0x0205ff80, 0x021f95b0, +4 more; loops (back edge at +0x2c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> native_data_0222f3c4 (image word 0x0222f3c4)
 *   back edge +0x2c -> +0x14
 *   branch +0x5c -> +0x68
 *   back edge +0x74 -> +0x48
 *   test +0x58 cmp r1, #127
 *   test +0x70 cmp r4, #12
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8418; the literal pool and
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

extern u8 native_data_0222f3c4[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f83e0(void);
extern void native_fn_0205ff9c(void);


asm u32 native_ov000_021f8418 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #32
    add r2, sp, #0
    mov r1, #8
    mov r0, #0
ov000_021f8418_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_021f8418_L14
    ldr r1, =native_data_0222f3c4
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0205ff80
    mov r4, #0
ov000_021f8418_L48:
    mov r0, r4
    bl native_fn_021f95b0
    bl native_fn_021f9614
    mov r1, r0
    cmp r1, #127
    beq ov000_021f8418_L68
    mov r0, r4
    bl native_fn_021f83e0
ov000_021f8418_L68:
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, #12
    blo ov000_021f8418_L48
    bl native_fn_0205ff9c
    add sp, sp, #32
    ldmia sp!, {r4, pc}
}
