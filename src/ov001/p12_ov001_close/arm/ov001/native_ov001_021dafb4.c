/* ov001 row 0x021dafb4: 108 bytes.
 *
 * What it does: 27 instructions; 6 call(s) to 0x021daffc, 0x02042c2c, 0x02028158, +3 more; loops (back edge at +0x1c); returns through pop {r4, pc}
 *
 * Decoded shape: loop with 6 calls (27 instructions, 6 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x10 -> +0x64
 *   branch +0x18 -> +0x48
 *   branch +0x44 -> +0x50
 *   test +0x0c cmp r1, #0
 *   test +0x14 cmp r1, #1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dafb4; the literal pool and
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

extern void native_fn_02042c2c(void);
extern void native_fn_02028158(void);
extern void native_fn_02026144(void);
extern void native_fn_02042104(void);
extern void native_fn_021dd010(void);


asm u32 native_ov001_021dafb4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrb r1, [r4, #0x430]
    cmp r1, #0
    beq ov001_021dafb4_L64
    cmp r1, #1
    bls ov001_021dafb4_L48
    bl native_fn_02042c2c
    ldr r1, [r4, #0x42c]
    sub r0, r1, r0
    bl native_fn_02028158
    ldrb r1, [r4, #0x430]
    bl native_fn_02026144
    mov r1, r0
    mov r0, r4
    mov r2, #0
    bl native_fn_02042104
    b ov001_021dafb4_L50
ov001_021dafb4_L48:
    ldr r1, [r4, #0x42c]
    bl native_fn_021dd010
ov001_021dafb4_L50:
    ldrb r1, [r4, #0x430]
    mov r0, #1
    sub r1, r1, #1
    strb r1, [r4, #0x430]
    ldmia sp!, {r4, pc}
ov001_021dafb4_L64:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
