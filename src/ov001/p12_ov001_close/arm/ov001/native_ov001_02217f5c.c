/* ov001 row 0x02217f5c: 108 bytes.
 *
 * What it does: 24 instructions; 1 call(s) to 0x02042b3c; loops (back edge at +0x34); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (24 instructions, 1 call, 2 branches, 1 back edge, 3 literal slots).
 *
 *   pool +0x60 -> constant 0x02242c4c (image word 0x02242c4c)
 *   pool +0x64 -> constant 0x02242c50 (image word 0x02242c50)
 *   pool +0x68 -> constant 0x02242cc0 (image word 0x02242cc0)
 *   branch +0x2c -> +0x54
 *   branch +0x3c -> +0x54
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmpne r1, #0
 *   test +0x28 cmpne r1, #0
 *   test +0x38 cmp r0, #0
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02217f5c; the literal pool and
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

extern void native_fn_02042b3c(void);


asm u32 native_ov001_02217f5c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #12
    ldr r0, =0x02242c4c
    mov r4, #0
    ldrb r0, [r0]
    cmp r0, #0
    ldrne r0, =0x02242c50
    ldrneb r1, [r0, #0x1e8]
    cmpne r1, #0
    ldrneb r1, [r0, #0x1e9]
    cmpne r1, #0
    beq ov001_02217f5c_L54
    add r1, sp, #0
    bl native_fn_02042b3c
    cmp r0, #0
    beq ov001_02217f5c_L54
    ldr r3, =0x02242cc0
    add r0, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r4, #1
ov001_02217f5c_L54:
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, pc}
}
