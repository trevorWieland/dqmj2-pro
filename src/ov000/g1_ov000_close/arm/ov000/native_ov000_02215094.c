/* ov000 row 0x02215094: 220 bytes.
 *
 * What it does: 55 instructions; 10 call(s) to 0x0205f998, 0x0205f8a0, 0x0205f98c, +7 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x6c -> +0x8c
 *   branch +0x88 -> +0xa4
 *   back edge +0xd0 -> +0x58
 *   test +0x68 cmp r4, #0
 *   test +0xcc cmp r4, #2
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215094; the literal pool and
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
extern void native_fn_0221750c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov000_02215094 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r9, r1
    mov r8, r2
    mov r7, r3
    bl native_fn_0205f998
    mov r2, #2
    mov r0, r10
    mov r1, #1
    strb r2, [r10, #0x22]
    bl native_fn_0205f8a0
    mov r10, r0
    mov r4, #0
    strh r4, [r10, #20]
    strh r4, [r10, #22]
    mov r0, #6
    strb r0, [r10, #0x20]
    mov r0, #2
    strb r0, [r10, #0x21]
    ldrb r6, [sp, #0x28]
    str r0, [r10]
    mov r11, #21
ov000_02215094_L58:
    ldr r0, [r10, #0x1c]
    and r1, r4, #255
    bl native_fn_0205f98c
    mov r5, r0
    cmp r4, #0
    bne ov000_02215094_L8c
    mov r1, r11
    bl native_fn_0221750c
    mov r0, r5
    mov r1, r9
    mov r2, r8
    bl native_fn_02048a60
    b ov000_02215094_La4
ov000_02215094_L8c:
    mov r1, #22
    bl native_fn_0221750c
    mov r0, r5
    mov r1, r7
    mov r2, r6
    bl native_fn_02048a60
ov000_02215094_La4:
    ldrb r1, [r10, #0x20]
    mov r0, r5
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    ldr r0, [r5, #0x7c]
    add r4, r4, #1
    bic r0, r0, #2
    str r0, [r5, #0x7c]
    cmp r4, #2
    blt ov000_02215094_L58
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
