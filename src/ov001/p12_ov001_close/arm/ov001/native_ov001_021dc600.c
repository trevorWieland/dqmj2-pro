/* ov001 row 0x021dc600: 164 bytes.
 *
 * What it does: 41 instructions; 6 call(s) to 0x02008e0c, 0x02008e0c, 0x02008e0c, +3 more; loops (back edge at +0x28); returns through pop {r4, r5, pc}
 *
 * Decoded shape: loop with 6 calls (41 instructions, 6 calls, 0 branches, 6 back edges, 0 literal slots).
 *
 *   test +0x10 cmpne r4, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc600; the literal pool and
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

extern void native_fn_02008e0c(void);


asm u32 native_ov001_021dc600 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #132
    mov r4, r1
    movs r5, r0
    cmpne r4, #0
    addeq sp, sp, #132
    ldmeqia sp!, {r4, r5, pc}
    add r1, sp, #10
    add r0, r5, #556
    mov r2, #120
    bl native_fn_02008e0c
    add r0, r4, #556
    add r1, r5, #556
    mov r2, #120
    bl native_fn_02008e0c
    add r0, sp, #10
    add r1, r4, #556
    mov r2, #120
    bl native_fn_02008e0c
    add r0, r5, #50
    add r1, sp, #0
    add r0, r0, #1024
    mov r2, #10
    bl native_fn_02008e0c
    add r0, r4, #50
    add r1, r5, #50
    add r0, r0, #1024
    add r1, r1, #1024
    mov r2, #10
    bl native_fn_02008e0c
    add r1, r4, #50
    add r0, sp, #0
    add r1, r1, #1024
    mov r2, #10
    bl native_fn_02008e0c
    ldrb r1, [r5, #0x43c]
    ldrb r0, [r4, #0x43c]
    strb r0, [r5, #0x43c]
    strb r1, [r4, #0x43c]
    add sp, sp, #132
    ldmia sp!, {r4, r5, pc}
}
