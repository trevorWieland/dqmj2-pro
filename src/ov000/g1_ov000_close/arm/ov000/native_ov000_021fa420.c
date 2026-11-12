/* ov000 row 0x021fa420: 120 bytes.
 *
 * What it does: 30 instructions; 4 call(s) to 0x02215698, 0x021f95b0, 0x021f9614, +1 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x5c
 *   branch +0x58 -> +0x70
 *   back edge +0x6c -> +0x14
 *   test +0x20 cmp r0, #127
 *   test +0x68 cmp r5, #12
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fa420; the literal pool and
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


asm u32 native_ov000_021fa420 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r4, r0
    bl ov000_display_context_02215698
    mov r6, #0
    mov r5, r6
ov000_021fa420_L14:
    and r0, r5, #255
    bl native_fn_021f95b0
    bl native_fn_021f9614
    cmp r0, #127
    bne ov000_021fa420_L5c
    mov r1, r5, lsr #31
    rsb r0, r1, r5, lsl #30
    add r0, r1, r0, ror #30
    mov r1, r5, asr #1
    mov r0, r0, lsl #24
    add r1, r5, r1, lsr #30
    mov r2, r0, asr #24
    mov r0, r1, lsl #22
    strh r2, [r4]
    mov r0, r0, asr #24
    strh r0, [r4, #2]
    mov r6, #1
    b ov000_021fa420_L70
ov000_021fa420_L5c:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #12
    blt ov000_021fa420_L14
ov000_021fa420_L70:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, pc}
}
