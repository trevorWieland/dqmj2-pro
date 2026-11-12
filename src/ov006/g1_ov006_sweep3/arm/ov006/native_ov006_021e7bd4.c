/* ov006 row 0x021e7bd4: 204 bytes.
 *
 * What it does: 50 instructions; 4 call(s) to 0x02049ae4, 0x02084e38, 0x02085270, +1 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xc8 -> constant 0x02218d90 (image word 0x02218d90)
 *   branch +0x28 -> +0xbc
 *   branch +0x74 -> +0xbc
 *   test +0x24 cmp r0, #0
 *   1 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e7bd4; the literal pool and
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

extern void native_fn_02049ae4(void);
extern void native_fn_02084e38(void);
extern void native_fn_02085270(void);
extern void native_fn_02086b14(void);


asm u32 native_ov006_021e7bd4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #16
    mov r8, r0
    mov r7, r1
    mov r6, r2
    mov r5, r3
    bl native_fn_02049ae4
    mov r4, r0
    ldr r0, [r4, #0x4]
    cmp r0, #0
    bne ov006_021e7bd4_Lbc
    add lr, sp, #12
    mov r12, #0
    ldr r0, =0x02218d90
    str r12, [lr]
    ldr r1, [r0, #0x78]
    ldrb r2, [sp, #0x28]
    mov r0, r1, asr #4
    add r0, r1, r0, lsr #27
    mov r0, r0, asr #5
    str r0, [sp, #0xc]
    mov r1, r5
    ldrb r3, [sp, #0x2c]
    stmia sp, {r12, lr}
    sub r5, r12, #1
    mov r0, r6
    str r5, [sp, #0x8]
    bl native_fn_02084e38
    movs r5, r0
    beq ov006_021e7bd4_Lbc
    mov r1, #0
    mov r2, r1
    add r0, r5, #60
    str r5, [r4, #0x4]
    bl native_fn_02085270
    mov r1, r8
    add r0, r5, #60
    blx r7
    ldr r1, [r5, #0x18]
    mov r0, r5
    orr r2, r1, #2
    mov r1, #10
    str r2, [r5, #0x18]
    bl native_fn_02086b14
    add sp, sp, #16
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov006_021e7bd4_Lbc:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
