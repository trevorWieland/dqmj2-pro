/* ov000 row 0x022017a8: 112 bytes.
 *
 * What it does: 27 instructions; 7 call(s) to 0x02215698, 0x02201990, 0x022156a4, +4 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x6c -> constant 0x02237d94 (image word 0x02237d94)
 *   branch +0x14 -> +0x28
 *   branch +0x24 -> +0x64
 *   branch +0x58 -> +0x64
 *   test +0x10 cmp r4, #14
 *   test +0x54 cmp r4, #15
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022017a8; the literal pool and
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
extern void native_fn_02201990(void);
extern void native_fn_022156a4(void);
extern void native_fn_02062074(void);
extern void native_fn_0221573c(void);
extern void native_fn_0221570c(void);
extern void native_fn_02219480(void);


asm u32 native_ov000_022017a8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r1
    mov r5, r0
    bl ov000_display_context_02215698
    cmp r4, #14
    bne ov000_022017a8_L28
    ldr r0, =0x02237d94
    mov r1, #4
    str r1, [r0]
    b ov000_022017a8_L64
ov000_022017a8_L28:
    mov r0, r5
    bl native_fn_02201990
    mov r0, #127
    bl native_fn_022156a4
    mov r0, #0
    bl native_fn_02062074
    mov r0, r4, lsl #24
    mov r0, r0, asr #24
    bl native_fn_0221573c
    mov r0, #1
    bl native_fn_0221570c
    cmp r4, #15
    beq ov000_022017a8_L64
    mov r0, #1
    bl native_fn_02219480
ov000_022017a8_L64:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
