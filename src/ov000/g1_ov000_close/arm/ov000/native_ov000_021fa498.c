/* ov000 row 0x021fa498: 536 bytes.
 *
 * What it does: 134 instructions; 23 call(s) to 0x02215698, 0x02066c3c, 0x021f95b0, +20 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x38 -> +0x174
 *   branch +0x170 -> +0x20c
 *   test +0x34 cmp r2, #2
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fa498; the literal pool and
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
extern void native_fn_02066c3c(void);
extern void native_fn_021f95b0(void);
extern void native_fn_021f9484(void);
extern void native_fn_02215984(void);
extern void native_fn_0205f98c(void);
extern void native_fn_02048a94(void);
extern void native_fn_0204b380(void);
extern void native_fn_021f8aac(void);
extern void native_fn_021f84a4(void);
extern void native_fn_021f85c8(void);
extern void native_fn_021f8f70(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021f9558(void);
extern void native_fn_021f9898(void);
extern void native_fn_0204b2d0(void);


asm u32 native_ov000_021fa498 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    bl native_fn_02215698
    mov r5, r0
    mov r6, #0
    bl native_fn_02066c3c
    mov r4, r0
    ldrb r0, [r5, #0x492]
    bl native_fn_021f95b0
    ldrb r2, [r4]
    add r3, r5, #184
    mov r1, #80
    mla r7, r0, r1, r3
    cmp r2, #2
    bne ov000_021fa498_L174
    ldrb r0, [r5, #0x493]
    bl native_fn_021f95b0
    add r1, r5, #1024
    ldrsb r3, [r1, #146]
    add r2, r5, #184
    mov r1, #80
    mla r4, r0, r1, r2
    mov r1, r3, lsr #31
    rsb r0, r1, r3, lsl #30
    add r1, r1, r0, ror #30
    mov r2, r3, asr #1
    add r0, r3, r2, lsr #30
    mov r2, r0, lsl #22
    mov r1, r1, lsl #24
    add r0, sp, #0
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_021f9484
    add r1, sp, #0
    mov r0, r4
    bl native_fn_02215984
    add r0, r5, #1024
    ldrsb r3, [r0, #147]
    add r0, sp, #0
    mov r2, r3, lsr #31
    rsb r1, r2, r3, lsl #30
    add r1, r2, r1, ror #30
    mov r1, r1, lsl #24
    mov r6, r1, asr #24
    mov r1, r3, asr #1
    add r1, r3, r1, lsr #30
    mov r1, r1, lsl #22
    mov r8, r1, asr #24
    mov r1, r6
    mov r2, r8
    bl native_fn_021f9484
    mov r0, r7
    add r1, sp, #0
    bl native_fn_02215984
    ldr r0, [r7, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldrb r1, [r7, #0x20]
    bl native_fn_02048a94
    strb r6, [r5, #0x490]
    add r0, r5, #132
    add r12, r0, #1024
    strb r8, [r5, #0x491]
    add r2, r5, #1024
    ldrsb r1, [r2, #146]
    add r0, r5, #16
    strb r1, [r4, #0x4c]
    ldrsb r3, [r2, #147]
    mov r1, #1
    strb r3, [r7, #0x4c]
    ldrsb r3, [r2, #147]
    ldrsb r6, [r2, #146]
    add r3, r5, r3
    ldrb r4, [r12, r6]
    ldrb r3, [r3, #0x484]
    strb r3, [r12, r6]
    ldrsb r2, [r2, #147]
    add r2, r5, r2
    strb r4, [r2, #0x484]
    bl native_fn_0204b380
    ldrb r0, [r5, #0x493]
    bl native_fn_021f95b0
    mov r1, #0
    bl native_fn_021f8aac
    bl native_fn_021f84a4
    bl native_fn_021f85c8
    bl native_fn_021f8f70
    mov r0, #104
    bl native_fn_021e7b9c
    mov r0, #4
    strb r0, [r5, #0x494]
    mov r6, #1
    b ov000_021fa498_L20c
ov000_021fa498_L174:
    ldrb r2, [r4, #0x1]
    add r0, sp, #0
    mov r1, r6
    sub r2, r2, #20
    strh r2, [sp]
    ldrb r2, [r4, #0x2]
    sub r2, r2, #20
    strh r2, [sp, #2]
    bl native_fn_021f9558
    ldr r0, [r7, #0x1c]
    mov r1, r6
    bl native_fn_0205f98c
    add r1, sp, #0
    mov r0, r7
    bl native_fn_02215984
    add r2, r5, #1024
    ldrb r0, [r4, #0x1]
    ldrb r1, [r4, #0x2]
    ldrsb r2, [r2, #147]
    bl native_fn_021f9898
    strb r0, [r5, #0x493]
    add r0, r5, #1024
    ldrsb r3, [r0, #147]
    add r0, sp, #0
    mov r2, r3, lsr #31
    rsb r1, r2, r3, lsl #30
    add r1, r2, r1, ror #30
    mov r2, r3, asr #1
    add r2, r3, r2, lsr #30
    mov r1, r1, lsl #24
    mov r2, r2, lsl #22
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_021f9484
    add r0, r5, #16
    mov r1, r6
    add r2, sp, #0
    bl native_fn_0204b2d0
ov000_021fa498_L20c:
    mov r0, r6
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
