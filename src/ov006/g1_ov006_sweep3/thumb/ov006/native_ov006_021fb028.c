/* ov006 row 0x021fb028: 88 bytes.
 *
 * What it does: 37 instructions; 3 call(s) to 0x020061ac, 0x022045e0, 0x0220374c; loops (back edge at +0x1c); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x50 -> native_data_0220dee8 (image word 0x0220dee8)
 *   pool +0x54 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb028; the literal pool and
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

extern u8 native_data_0220dee8[];
extern void native_fn_020061ac(void);
extern void native_fn_022045e0(void);
extern void native_fn_0220374c(void);


asm u32 native_ov006_021fb028 (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x3c
    add r3, r0, #0x0
    ldrb r0, [r3, #0x1]
    add r4, r1, #0x0
    ldr r2, =native_data_0220dee8
    str r0, [sp]
    ldrb r0, [r3, #0x2]
    mov r1, #0x10
    str r0, [sp, #0x4]
    ldrb r0, [r3, #0x3]
    str r0, [sp, #0x8]
    ldrb r3, [r3, #0]
    add r0, sp, #0xc
    blx native_fn_020061ac
    add r0, sp, #0x1c
    add r1, sp, #0xc
    mov r2, #0x10
    bl native_fn_022045e0
    mov r0, #0x7
    str r0, [sp]
    add r0, sp, #0x1c
    str r0, [sp, #0x4]
    mov r0, #0x1
    str r0, [sp, #0x8]
    ldr r0, =0x0221c0ec
    mov r2, #0x1d
    ldr r0, [r0, #0x8]
    mul r2, r4
    ldr r0, [r0, #0x14]
    mov r1, #0x5f
    add r2, #0x8
    mov r3, #0x2
    bl native_fn_0220374c
    add sp, #0x3c
    pop {r3, r4, pc}
    mov r8, r8
}
