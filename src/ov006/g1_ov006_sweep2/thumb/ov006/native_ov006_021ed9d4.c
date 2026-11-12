/* ov006 row 0x021ed9d4: 122 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0x22
 *   branch +0x2c -> +0x3c
 *   back edge +0x66 -> +0x3e
 *   test +0x2a cmp r0, #0x0
 *   test +0x64 cmp r4, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed9d4; the literal pool and
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

extern void native_fn_021ebb1c(void);
extern void native_fn_021ebb2c(void);
extern void native_fn_021eda50(void);
extern void native_fn_021eda84(void);
extern void native_fn_021edaa8(void);


asm u32 native_ov006_021ed9d4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    add r5, r1, #0x0
    add r7, r0, #0x0
    lsr r0, r5, #0x1f
    add r0, r5, r0
    asr r0, r0, #0x1
    str r2, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_021ebb1c
    add r6, r0, #0x0
    bne ov006_021ed9d4_L22
    mov r0, #0x0
    add sp, #0x10
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed9d4_L22:
    add r0, r5, #0x0
    bl native_fn_021ebb1c
    str r0, [sp, #0xc]
    cmp r0, #0x0
    bne ov006_021ed9d4_L3c
    add r0, r6, #0x0
    bl native_fn_021ebb2c
    mov r0, #0x0
    add sp, #0x10
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021ed9d4_L3c:
    mov r4, #0x0
ov006_021ed9d4_L3e:
    ldr r0, [sp, #0x8]
    ldr r3, [sp, #0x4]
    str r0, [sp]
    add r0, r4, #0x0
    add r1, r6, #0x0
    add r2, r5, #0x0
    bl native_fn_021eda50
    add r0, r6, #0x0
    add r1, r7, #0x0
    add r2, r5, #0x0
    bl native_fn_021eda84
    ldr r2, [sp, #0xc]
    add r0, r7, #0x0
    add r1, r5, #0x0
    bl native_fn_021edaa8
    add r4, r4, #0x1
    cmp r4, #0x2
    blt ov006_021ed9d4_L3e
    add r0, r6, #0x0
    bl native_fn_021ebb2c
    ldr r0, [sp, #0xc]
    bl native_fn_021ebb2c
    mov r0, #0x0
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
}
