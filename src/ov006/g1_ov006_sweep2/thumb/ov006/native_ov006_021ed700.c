/* ov006 row 0x021ed700: 104 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> constant 0x00005790 (image word 0x00005790)
 *   pool +0x60 -> constant 0x02219b4c (image word 0x02219b4c)
 *   pool +0x64 -> constant 0x02219b6c (image word 0x02219b6c)
 *   branch +0x32 -> +0x3e
 *   branch +0x3c -> +0x44
 *   test +0x30 cmp r4, #0xff
 *   test +0x3a cmp r0, #0x0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed700; the literal pool and
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

extern void native_fn_021edbac(void);
extern void native_fn_021edc78(void);
extern void native_fn_021edc50(void);
extern void native_fn_021edc20(void);


asm u32 native_ov006_021ed700 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    add r5, r0, #0x0
    add r6, r1, #0x0
    add r4, r2, #0x0
    add r0, sp, #0x8
    mov r1, #0x0
    mov r2, #0x8
    add r7, r3, #0x0
    bl native_fn_021edbac
    mov r1, #0x2
    add r0, sp, #0x8
    strb r1, [r0, #0x1]
    ldr r0, =0x00005790
    bl native_fn_021edc78
    add r1, sp, #0x8
    strh r0, [r1, #0x2]
    ldr r0, =0x02219b4c
    ldr r0, [r0, #0x34]
    bl native_fn_021edc50
    str r0, [sp, #0xc]
    cmp r4, #0xff
    beq ov006_021ed700_L3e
    ldr r1, =0x02219b6c
    mov r0, #0x1c
    ldrsb r0, [r1, r0]
    cmp r0, #0x0
    bne ov006_021ed700_L44
ov006_021ed700_L3e:
    mov r0, #0x0
    mvn r0, r0
    str r0, [sp, #0xc]
ov006_021ed700_L44:
    add r0, sp, #0x8
    str r0, [sp]
    mov r0, #0x8
    str r0, [sp, #0x4]
    add r0, r7, #0x0
    add r1, r5, #0x0
    add r2, r6, #0x0
    mov r3, #0x0
    bl native_fn_021edc20
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
}
