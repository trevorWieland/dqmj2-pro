/* ov006 row 0x021eef58: 188 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xac -> native_data4_0221aad0 (image word 0x0221aad0)
 *   pool +0xb0 -> constant 0x0000231f (image word 0x0000231f)
 *   pool +0xb4 -> constant 0x0221ab50 (image word 0x0221ab50)
 *   pool +0xb8 -> native_fn_021ee9a4+1 (image word 0x021ee9a5)
 *   branch +0x54 -> +0x74
 *   branch +0x62 -> +0x6e
 *   branch +0x7a -> +0xa2
 *   branch +0x86 -> +0x92
 *   test +0x52 cmp r0, #0x0
 *   test +0x60 cmp r0, #0x0
 *   test +0x78 cmp r1, #0x1
 *   test +0x84 cmp r0, #0x3
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eef58; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02007ff4(void);
extern u8 native_data4_0221aad0[];
extern void native_fn_02089aa4(void);
extern void native_fn_02008008(void);
extern void native_fn_021ee9a4(void);
extern void native_fn_02089ba0(void);


asm u32 native_ov006_021eef58 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r1, #0x0
    add r7, r0, #0x0
    str r2, [sp]
    blx native_fn_02007ff4
    add r4, r0, #0x0
    add r0, r5, #0x0
    ldr r2, =native_data4_0221aad0
    add r0, #0x63
    mov r1, #0x3
    bic r0, r1
    add r6, r0, #0x0
    str r5, [r2, #0x28]
    add r6, #0x2f
    mov r1, #0x1f
    ldr r3, =0x0000231f
    str r0, [r2, #0x8]
    bic r6, r1
    str r6, [r2, #0x3c]
    add r6, r6, r3
    bic r6, r1
    str r6, [r2, #0x4c]
    add r6, #0xdf
    bic r6, r1
    str r6, [r0, #0x4]
    ldr r1, [sp]
    ldr r0, [r2, #0x8]
    add r5, r5, r1
    ldr r1, [r0, #0x4]
    sub r1, r5, r1
    str r1, [r0, #0x8]
    ldr r0, [r2, #0x8]
    mov r1, #0x0
    str r1, [r0, #0xc]
    ldr r0, [r2, #0x8]
    mov r1, #0x3
    str r1, [r0, #0]
    ldr r0, =0x0221ab50
    str r7, [r0, #0]
    ldr r0, [r2, #0x2c]
    cmp r0, #0x0
    bne ov006_021eef58_L74
    sub r3, #0x1f
    ldr r0, [r2, #0x3c]
    add r1, r3, #0x0
    bl native_fn_02089aa4
    cmp r0, #0x0
    beq ov006_021eef58_L6e
    add r0, r4, #0x0
    blx native_fn_02008008
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021eef58_L6e:
    ldr r0, =native_data4_0221aad0
    mov r1, #0x1
    str r1, [r0, #0x2c]
ov006_021eef58_L74:
    ldr r0, =native_data4_0221aad0
    ldr r1, [r0, #0x2c]
    cmp r1, #0x1
    bne ov006_021eef58_La2
    ldr r0, [r0, #0x8]
    ldr r1, =native_fn_021ee9a4+1
    bl native_fn_02089ba0
    cmp r0, #0x3
    beq ov006_021eef58_L92
    add r0, r4, #0x0
    blx native_fn_02008008
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021eef58_L92:
    ldr r0, =native_data4_0221aad0
    mov r1, #0x4
    str r1, [r0, #0x2c]
    add r0, r4, #0x0
    blx native_fn_02008008
    mov r0, #0x1
    pop {r3, r4, r5, r6, r7, pc}
ov006_021eef58_La2:
    add r0, r4, #0x0
    blx native_fn_02008008
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
}
