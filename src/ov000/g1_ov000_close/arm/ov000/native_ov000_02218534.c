/* ov000 row 0x02218534: 128 bytes.
 *
 * What it does: 28 instructions; 3 call(s) to 0x02048404, 0x02048404, 0x0204854c; loops (back edge at +0x1c); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> native_data_0222fa7c (image word 0x0222fa7c)
 *   pool +0x74 -> native_data_0222fa08 (image word 0x0222fa08)
 *   pool +0x78 -> native_data_0222fa94 (image word 0x0222fa94)
 *   pool +0x7c -> constant 0x02245e54 (image word 0x02245e54)
 *   branch +0x0c -> +0x28
 *   branch +0x24 -> +0x3c
 *   test +0x04 cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218534; the literal pool and
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

extern u8 native_data_0222fa7c[];
extern void native_fn_02048404(void);
extern u8 native_data_0222fa08[];
extern u8 native_data_0222fa94[];
extern void native_fn_0204854c(void);


asm u32 native_ov000_02218534 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #0
    mov r0, #1
    bne ov000_02218534_L28
    ldr r1, =native_data_0222fa7c
    mov r2, #4
    mov r3, #2
    bl native_fn_02048404
    ldr r1, =native_data_0222fa08
    b ov000_02218534_L3c
ov000_02218534_L28:
    ldr r1, =native_data_0222fa94
    mov r2, #4
    mov r3, #2
    bl native_fn_02048404
    ldr r1, =native_data_0222fa08
ov000_02218534_L3c:
    strb r0, [r1, #0x3]
    ldr r1, =native_data_0222fa08
    mov r0, #1
    ldrb r1, [r1, #0x3]
    bl native_fn_0204854c
    ldr r2, =0x02245e54
    ldr r1, =native_data_0222fa08
    str r0, [r2, #0x8]
    ldr r3, [r0, #0x4]
    mov r0, #0
    str r3, [r2, #0x24]
    strb r0, [r1]
    ldmia sp!, {r3, pc}
}
