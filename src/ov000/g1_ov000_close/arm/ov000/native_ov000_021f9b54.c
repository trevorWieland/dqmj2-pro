/* ov000 row 0x021f9b54: 264 bytes.
 *
 * What it does: 65 instructions; 18 call(s) to 0x02215698, 0x02217440, 0x02063358, +15 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x104 -> constant 0x02236f14 (image word 0x02236f14)
 *   branch +0x2c -> +0xe0
 *   branch +0x34 -> +0x78
 *   branch +0x4c -> +0x70
 *   branch +0xb4 -> +0xc0
 *   branch +0xdc -> +0xf8
 *   test +0x28 cmp r0, #0
 *   test +0x30 cmp r4, #127
 *   test +0x48 cmp r0, #0
 *   test +0x7c cmp r0, #127
 *   test +0xb0 cmp r0, #127
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9b54; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02217440(void);
extern void native_fn_02063358(void);
extern void native_fn_021fa420(void);
extern void native_fn_02063280(void);
extern void native_fn_02063348(void);
extern void native_fn_022156fc(void);
extern void native_fn_02062aa0(void);
extern void native_fn_021f8134(void);
extern void native_fn_021f82c4(void);
extern void native_fn_021f90cc(void);
extern void native_fn_021f8f70(void);
extern void native_fn_0204b380(void);
extern void native_fn_020620b4(void);
extern void native_fn_0221767c(void);
extern void native_fn_021f85c8(void);
extern void native_fn_021f84a0(void);


asm u32 native_ov000_021f9b54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #4
    bl native_fn_02215698
    mov r5, r0
    bl native_fn_02217440
    bl native_fn_02063358
    ldr r1, =0x02236f14
    mov r4, r0
    ldr r0, [r1, #0x8]
    mov r6, #0
    cmp r0, #0
    bne ov000_021f9b54_Le0
    cmp r4, #127
    beq ov000_021f9b54_L78
    add r0, sp, #0
    strh r6, [r0]
    strh r6, [r0, #2]
    bl native_fn_021fa420
    cmp r0, #0
    beq ov000_021f9b54_L70
    ldrsh r2, [sp]
    ldrsh r0, [sp, #2]
    mov r1, r4
    add r0, r2, r0, lsl #2
    and r0, r0, #255
    add r2, r5, r0
    strb r4, [r2, #0x478]
    bl native_fn_02063280
ov000_021f9b54_L70:
    mov r0, #127
    bl native_fn_02063348
ov000_021f9b54_L78:
    bl native_fn_022156fc
    cmp r0, #127
    moveq r0, #0
    streqb r0, [r5, #0x49b]
    bl native_fn_02062aa0
    strb r0, [r5, #0x495]
    bl native_fn_021f8134
    bl native_fn_021f82c4
    bl native_fn_021f90cc
    bl native_fn_021f8f70
    add r0, r5, #16
    mov r1, #1
    bl native_fn_0204b380
    bl native_fn_022156fc
    cmp r0, #127
    beq ov000_021f9b54_Lc0
    mov r0, #0
    bl native_fn_020620b4
ov000_021f9b54_Lc0:
    ldr r0, =0x02236f14
    mov r1, #127
    strb r1, [r0]
    bl native_fn_0221767c
    ldr r0, =0x02236f14
    mov r1, #10
    str r1, [r0, #0x8]
    b ov000_021f9b54_Lf8
ov000_021f9b54_Le0:
    bl native_fn_021f85c8
    mov r1, r6
    ldr r0, =0x02236f14
    mov r6, #1
    str r1, [r0, #0x8]
    bl native_fn_021f84a0
ov000_021f9b54_Lf8:
    mov r0, r6
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, pc}
}
