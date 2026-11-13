/* ov000 row 0x021f8044: 240 bytes.
 *
 * What it does: 60 instructions; 14 call(s) to 0x02215698, 0x021f8838, 0x0221767c, +11 more; loops (back edge at +0x70); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0xa0 -> +0xc0
 *   branch +0xbc -> +0xd8
 *   back edge +0xe4 -> +0x2c
 *   test +0x9c cmp r8, #127
 *   test +0xe0 cmp r10, #12
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8044; the literal pool and
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
extern void native_fn_021f8838(void);
extern void native_fn_0221767c(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9614(void);
extern void native_fn_021f9484(void);
extern void native_fn_0205f998(void);
extern void native_fn_022158c8(void);
extern void native_fn_021f94b4(void);
extern void native_fn_021f950c(void);
extern void native_fn_0205f98c(void);
extern void native_fn_021f84a4(void);


asm u32 native_ov000_021f8044 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    bl ov000_display_context_02215698
    mov r4, r0
    bl native_fn_021f8838
    bl native_fn_0221767c
    add r6, r4, #184
    mov r10, #0
    sub r5, sp, #4
    add r7, sp, #0
    mov r11, #12
    mov r4, #80
ov000_021f8044_L2c:
    mov r0, r10
    bl native_fn_021f95b0
    bl native_fn_021f9614
    mov r2, r10, lsr #31
    rsb r1, r2, r10, lsl #30
    add r1, r2, r1, ror #30
    mov r1, r1, lsl #24
    mov r2, r10, lsl #22
    mov r8, r0
    mov r0, r7
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_021f9484
    mov r0, r10
    bl native_fn_021f95b0
    mla r9, r0, r4, r6
    mov r0, r9
    bl native_fn_0205f998
    ldrh r12, [sp]
    ldrh r1, [sp, #2]
    mov r0, r9
    mov r2, r11
    strh r12, [r5]
    strh r1, [r5, #2]
    ldr r1, [r5]
    mov r3, #0
    bl native_fn_022158c8
    strb r10, [r9, #0x4c]
    cmp r8, #127
    beq ov000_021f8044_Lc0
    mov r0, r8
    bl native_fn_021f94b4
    strb r0, [r9, #0x4e]
    and r1, r0, #255
    mov r0, r9
    bl native_fn_021f950c
    b ov000_021f8044_Ld8
ov000_021f8044_Lc0:
    ldr r0, [r9, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldr r1, [r0, #0x7c]
    bic r1, r1, #2
    str r1, [r0, #0x7c]
ov000_021f8044_Ld8:
    add r0, r10, #1
    and r10, r0, #255
    cmp r10, #12
    blo ov000_021f8044_L2c
    bl native_fn_021f84a4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
