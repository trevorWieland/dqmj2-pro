/* ov000 row 0x02215170: 340 bytes.
 *
 * What it does: 85 instructions; 14 call(s) to 0x0205f998, 0x0205f8a0, 0x0205f98c, +11 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x148 -> +0xbc
 *   test +0xd0 cmp r5, #1
 *   test +0xec cmp r5, #1
 *   test +0x144 cmp r5, #3
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215170; the literal pool and
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

extern void native_fn_0205f998(void);
extern void native_fn_0205f8a0(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048f5c(void);
extern void native_fn_0221750c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov000_02215170 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r5, r1
    mov r9, r2
    bl native_fn_0205f998
    mov r3, #3
    mov r0, r10
    mov r1, #1
    mov r2, #2
    strb r3, [r10, #0x22]
    bl native_fn_0205f8a0
    mov r10, r0
    ldr r0, [r10, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    mov r4, r0
    mov r0, #0
    strh r0, [r10, #20]
    strh r0, [r10, #22]
    mov r0, #5
    strb r0, [r10, #0x20]
    mov r0, #1
    bl native_fn_02048f5c
    strb r0, [r10, #0x21]
    mov r0, #3
    str r0, [r10]
    mov r0, r4
    mov r1, #62
    bl native_fn_0221750c
    mov r0, r4
    mov r1, r5
    mov r2, r9
    bl native_fn_02048a60
    ldrb r1, [r10, #0x20]
    mov r0, r4
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r4
    bl native_fn_02048a9c
    add r0, r5, #56
    and r7, r0, #255
    ldr r0, [r4, #0x7c]
    mov r5, #1
    orr r0, r0, #2
    str r0, [r4, #0x7c]
    mov r4, #4
    mov r11, #2
ov000_02215170_Lbc:
    ldr r0, [r10, #0x1c]
    mov r1, r5
    bl native_fn_0205f98c
    strb r4, [r10, #0x20]
    mov r8, r0
    cmp r5, #1
    moveq r0, #0
    movne r0, #8
    add r1, r9, r0
    strb r11, [r10, #0x21]
    mov r0, #3
    str r0, [r10]
    cmp r5, #1
    moveq r0, #60
    movne r0, #61
    and r6, r1, #255
    and r1, r0, #255
    mov r0, r8
    bl native_fn_0221750c
    mov r2, r6
    mov r0, r8
    mov r1, r7
    bl native_fn_02048a60
    ldrb r1, [r10, #0x20]
    mov r0, r8
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r8
    bl native_fn_02048a9c
    ldr r1, [r8, #0x7c]
    add r0, r5, #1
    bic r1, r1, #2
    and r5, r0, #255
    str r1, [r8, #0x7c]
    cmp r5, #3
    blo ov000_02215170_Lbc
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
