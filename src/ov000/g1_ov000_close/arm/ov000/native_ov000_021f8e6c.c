/* ov000 row 0x021f8e6c: 260 bytes.
 *
 * What it does: 64 instructions; 8 call(s) to 0x02215698, 0x0205f98c, 0x021f95c8, +5 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x100 -> constant 0x02236f2c (image word 0x02236f2c)
 *   branch +0x68 -> +0x7c
 *   test +0x4c cmp r1, #0
 *   test +0x58 cmp r1, #0
 *   test +0x5c cmpne r0, #127
 *   test +0x64 cmpne r1, #127
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8e6c; the literal pool and
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
extern void native_fn_0205f98c(void);
extern void native_fn_021f95c8(void);
extern void native_fn_0205fb3c(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a60(void);
extern void native_fn_0205f9e4(void);


asm u32 native_ov000_021f8e6c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r4, r0
    bl native_fn_02215698
    ldr r2, =0x02236f2c
    mov r1, #72
    mla r5, r4, r1, r2
    mov r4, r0
    ldr r0, [r5, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldr r1, [r5, #0x34]
    mov r6, r0
    add r3, sp, #0
    mov r2, #0
    and r0, r1, #255
    strh r2, [r3]
    strh r2, [r3, #2]
    bl native_fn_021f95c8
    ldr r1, [r5, #0x1c]
    cmp r1, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldrb r1, [r5, #0x23]
    cmp r1, #0
    cmpne r0, #127
    ldrne r1, [r5, #0x34]
    cmpne r1, #127
    bne ov000_021f8e6c_L7c
    ldr r0, [r6, #0x7c]
    bic r0, r0, #2
    str r0, [r6, #0x7c]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
ov000_021f8e6c_L7c:
    add r2, r4, #184
    mov r1, #80
    mla r7, r0, r1, r2
    ldr r0, [r7, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    mov r4, r0
    mov r0, r5
    mov r1, #2
    bl native_fn_0205fb3c
    ldrh r2, [r7, #72]
    ldrh r1, [r7, #74]
    mov r0, r6
    strh r2, [sp]
    strh r1, [sp, #2]
    ldrb r1, [r4, #0x78]
    sub r1, r1, #2
    and r1, r1, #255
    bl native_fn_02048a94
    ldr r1, [r6, #0x7c]
    mov r0, r6
    orr r1, r1, #2
    str r1, [r6, #0x7c]
    ldrsh r2, [sp, #2]
    ldrsh r1, [sp]
    add r2, r2, #2
    bl native_fn_02048a60
    ldr r1, [r6, #0x7c]
    mov r0, r5
    orr r1, r1, #2
    str r1, [r6, #0x7c]
    bl native_fn_0205f9e4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
