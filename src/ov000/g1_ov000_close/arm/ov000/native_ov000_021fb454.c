/* ov000 row 0x021fb454: 404 bytes.
 *
 * What it does: 99 instructions; 7 call(s) to 0x021fb97c, 0x02215d94, 0x0207c18c, +4 more; loops (back edge at +0x80); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x18c -> constant 0x02237178 (image word 0x02237178)
 *   pool +0x190 -> constant 0x02237170 (image word 0x02237170)
 *   branch +0x24 -> +0x50
 *   branch +0x4c -> +0x88
 *   branch +0xac -> +0x180
 *   branch +0xec -> +0x104
 *   branch +0x108 -> +0x12c
 *   branch +0x128 -> +0x14c
 *   test +0x38 cmp r0, #0
 *   test +0x60 cmp r0, #0
 *   test +0xa8 cmp r0, #255
 *   test +0xe0 cmp r1, r8
 *   test +0xf4 cmp r0, #0
 *   test +0x104 cmp r10, #0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fb454; the literal pool and
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

extern void native_fn_021fb97c(void);
extern void native_fn_02215d94(void);
extern void native_fn_0207c18c(void);
extern void native_fn_021fb8f8(void);
extern void native_fn_021fb9a8(void);


asm u32 native_ov000_021fb454 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mov r6, #0
    movs r10, r3
    str r0, [sp]
    str r1, [sp, #0x4]
    str r2, [sp, #0x8]
    mov r5, r6
    ldr r4, [sp, #0x38]
    beq ov000_021fb454_L50
    mov r0, #52
    mul r1, r4, r0
    ldrb r0, [r10, r1]
    add r5, r10, r1
    cmp r0, #0
    addeq sp, sp, #16
    moveq r0, r6
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r11, [r5, #0x4]
    b ov000_021fb454_L88
ov000_021fb454_L50:
    mov r0, r4
    bl native_fn_021fb97c
    mov r6, r0
    ldrb r0, [r6, #0x33]
    cmp r0, #0
    addne sp, sp, #16
    movne r0, r5
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, r4
    bl native_fn_02215d94
    mov r1, r0
    add r0, r6, #32
    bl native_fn_0207c18c
    mov r11, r0
ov000_021fb454_L88:
    mov r0, #52
    mul r3, r4, r0
    ldr r2, =0x02237178
    ldr r0, [sp]
    ldr r8, [r2, r3]
    mov r1, r10
    bl native_fn_021fb8f8
    str r0, [sp, #0xc]
    cmp r0, #255
    beq ov000_021fb454_L180
    ldr r0, [sp, #0xc]
    mov r1, #52
    mul r9, r0, r1
    ldr r4, =0x02237170
    ldr r1, [sp]
    add r0, r4, r9
    bl native_fn_021fb9a8
    ldrsh r7, [r0]
    ldr r1, [sp]
    add r0, r4, r9
    bl native_fn_021fb9a8
    add r1, r7, r11
    cmp r1, r8
    ldrsh r4, [r0, #2]
    subge r7, r8, r11
    bge ov000_021fb454_L104
    ldrb r0, [sp, #0x3c]
    cmp r0, #0
    addne sp, sp, #16
    movne r0, #0
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021fb454_L104:
    cmp r10, #0
    beq ov000_021fb454_L12c
    add r1, r10, #12
    ldr r0, [r1, r9]
    sub r0, r0, r4
    str r0, [r1, r9]
    ldr r0, [r5, #0x4]
    add r0, r0, r7
    str r0, [r5, #0x4]
    b ov000_021fb454_L14c
ov000_021fb454_L12c:
    ldr r0, [sp, #0xc]
    bl native_fn_021fb97c
    ldrsh r1, [r0, #38]
    sub r1, r1, r4
    strh r1, [r0, #38]
    ldrsh r0, [r6, #36]
    add r0, r0, r7
    strh r0, [r6, #36]
ov000_021fb454_L14c:
    ldr r0, [sp, #0x4]
    ldr r1, [r0]
    mov r0, #1
    add r2, r1, r4
    ldr r1, [sp, #0x4]
    str r2, [r1]
    ldr r1, [sp, #0x8]
    ldr r1, [r1]
    add r2, r1, r7
    ldr r1, [sp, #0x8]
    add sp, sp, #16
    str r2, [r1]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021fb454_L180:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
