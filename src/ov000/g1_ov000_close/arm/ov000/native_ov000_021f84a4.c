/* ov000 row 0x021f84a4: 128 bytes.
 *
 * What it does: 32 instructions; 8 call(s) to 0x02215698, 0x021f95b0, 0x021f9614, +5 more; loops (back edge at +0x74); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x4c -> +0x60
 *   branch +0x5c -> +0x68
 *   back edge +0x74 -> +0x10
 *   test +0x48 cmp r7, #127
 *   test +0x70 cmp r6, #12
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f84a4; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f9484(void);
extern void native_fn_021f8524(void);
extern void native_fn_021f8588(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_021f84a4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl ov000_display_context_02215698
    mov r6, #0
    add r4, sp, #0
ov000_021f84a4_L10:
    mov r0, r6
    bl native_fn_021f95b0
    mov r5, r0
    bl native_fn_021f9614
    mov r2, r6, lsr #31
    rsb r1, r2, r6, lsl #30
    add r1, r2, r1, ror #30
    mov r1, r1, lsl #24
    mov r2, r6, lsl #22
    mov r7, r0
    mov r0, r4
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_021f9484
    cmp r7, #127
    beq ov000_021f84a4_L60
    mov r0, r5
    mov r1, r4
    bl native_fn_021f8524
    b ov000_021f84a4_L68
ov000_021f84a4_L60:
    mov r0, r4
    bl native_fn_021f8588
ov000_021f84a4_L68:
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, #12
    blo ov000_021f84a4_L10
    bl native_fn_02048308
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
