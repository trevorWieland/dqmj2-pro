/* ov000 row 0x02208ff8: 264 bytes.
 *
 * What it does: 66 instructions; 4 call(s) to 0x02208fb4, 0x0202a37c, 0x02208fb4, +1 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1c -> +0xfc
 *   branch +0x44 -> +0xfc
 *   branch +0x98 -> +0xf8
 *   test +0x40 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02208ff8; the literal pool and
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

extern void native_fn_02208fb4(void);
extern void native_fn_0202a37c(void);
extern void native_fn_020363d0(void);


asm u32 native_ov000_02208ff8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #16
    movs r2, #1
    mov r5, r0
    mov r4, r1
    str r2, [r5, #0x60]
    mov r6, #0
    beq ov000_02208ff8_Lfc
    mov r0, #4
    str r0, [sp]
    ldrb r1, [r5, #0x5e]
    ldrb r2, [r5, #0x5f]
    ldr r3, [r5, #0x50]
    mov r0, r4
    bl native_fn_02208fb4
    str r0, [r5, #0x40]
    cmp r0, #0
    beq ov000_02208ff8_Lfc
    ldrb r1, [r5, #0x5e]
    ldrb r2, [r5, #0x5f]
    mov r0, r4
    mov r1, r1, lsl #5
    mul r1, r2, r1
    mov r2, #4
    bl native_fn_0202a37c
    add r1, r0, #3
    str r0, [r5, #0x48]
    bic r0, r1, #3
    str r0, [r5, #0x4c]
    mov r0, #4
    str r0, [sp]
    ldrb r1, [r5, #0x5e]
    ldrb r2, [r5, #0x5f]
    ldr r3, [r5, #0x4c]
    mov r0, r4
    bl native_fn_02208fb4
    str r0, [r5, #0x44]
    cmp r0, #0
    beq ov000_02208ff8_Lf8
    ldrb r1, [r5, #0x5d]
    mov r0, #32
    str r1, [sp]
    str r0, [sp, #0x4]
    ldr r0, [r5, #0x58]
    str r0, [sp, #0x8]
    ldrb r0, [r5, #0x84]
    str r0, [sp, #0xc]
    ldrb r1, [r5, #0x5e]
    ldrb r2, [r5, #0x5f]
    ldrb r3, [r5, #0x5c]
    ldr r0, [r5, #0x54]
    bl native_fn_020363d0
    ldr r0, [r5, #0x40]
    mov r1, r6
    ldr r2, [r0, #0x14]
    ldr r2, [r2, #0x4]
    blx r2
    ldr r0, [r5, #0x44]
    mov r1, r6
    ldr r2, [r0, #0x14]
    ldr r2, [r2, #0x4]
    blx r2
ov000_02208ff8_Lf8:
    mov r6, #1
ov000_02208ff8_Lfc:
    mov r0, r6
    add sp, sp, #16
    ldmia sp!, {r4, r5, r6, pc}
}
