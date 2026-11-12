/* ov000 row 0x021f3f88: 100 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x021f3cd0, 0x0200103c, 0x02041f48; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x20 -> +0x58
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3f88; the literal pool and
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

extern void native_fn_021f3cd0(void);
extern void native_fn_0200103c(void);
extern void native_fn_02041f48(void);


asm u32 native_ov000_021f3f88 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #12
    mov r8, r1
    mov r7, r2
    mov r6, r3
    mov r5, #0
    bl native_fn_021f3cd0
    movs r4, r0
    beq ov000_021f3f88_L58
    add r0, sp, #0
    str r8, [sp]
    mov r2, r0
    str r7, [sp, #0x4]
    str r6, [sp, #0x8]
    add r1, r4, #148
    bl native_fn_0200103c
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, r4
    bl native_fn_02041f48
    add r5, r4, #112
ov000_021f3f88_L58:
    mov r0, r5
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
