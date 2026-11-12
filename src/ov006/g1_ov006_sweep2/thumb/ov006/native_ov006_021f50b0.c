/* ov006 row 0x021f50b0: 460 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1a0 -> constant 0xffffe0ff (image word 0xffffe0ff)
 *   pool +0x1a4 -> constant 0xffff1fff (image word 0xffff1fff)
 *   pool +0x1a8 -> constant 0xffcfffef (image word 0xffcfffef)
 *   pool +0x1ac -> constant 0x00200010 (image word 0x00200010)
 *   pool +0x1b0 -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x1b4 -> constant 0x04000008 (image word 0x04000008)
 *   pool +0x1b8 -> constant 0x00000d08 (image word 0x00000d08)
 *   pool +0x1bc -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x1c0 -> constant 0xc7ffffff (image word 0xc7ffffff)
 *   pool +0x1c4 -> constant 0x04000304 (image word 0x04000304)
 *   pool +0x1c8 -> constant 0xffff7fff (image word 0xffff7fff)
 *   0 block transfer(s), 34 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f50b0; the literal pool and
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

extern void native_fn_02002be0(void);
extern void native_fn_02002e5c(void);
extern void native_fn_020030ec(void);
extern void native_fn_02002c98(void);
extern void native_fn_02002d1c(void);
extern void native_fn_020042e0(void);
extern void native_fn_020038a8(void);
extern void native_fn_02003950(void);
extern void native_fn_02002d00(void);
extern void native_fn_02203338(void);
extern void native_fn_022042c4(void);
extern void native_fn_022043f4(void);
extern void native_fn_02202b84(void);
extern void native_fn_02002c50(void);


asm u32 native_ov006_021f50b0 (register u32 a0)
{
    push {r4, r5, r6, lr}
    mov r0, #0x0
    blx native_fn_02002be0
    mov r0, #0x1
    blx native_fn_02002e5c
    mov r0, #0x2
    blx native_fn_020030ec
    mov r1, #0x0
    mov r0, #0x1
    add r2, r1, #0x0
    blx native_fn_02002c98
    mov r0, #0x1
    lsl r0, r0, #0x1a
    ldr r2, [r0, #0]
    ldr r1, =0xffffe0ff
    and r1, r2
    str r1, [r0, #0]
    ldr r2, [r0, #0]
    ldr r1, =0xffff1fff
    and r1, r2
    str r1, [r0, #0]
    add r0, #0x6c
    mov r1, #0x0
    blx native_fn_02002d1c
    mov r0, #0x1
    lsl r0, r0, #0x1a
    add r3, r0, #0x0
    ldr r2, [r0, #0]
    ldr r1, =0xffcfffef
    add r3, #0x8
    and r2, r1
    ldr r1, =0x00200010
    orr r1, r2
    str r1, [r0, #0]
    ldrh r2, [r3, #0]
    mov r1, #0x40
    bic r2, r1
    strh r2, [r3, #0]
    add r3, r0, #0x0
    add r3, #0xa
    ldrh r2, [r3, #0]
    bic r2, r1
    strh r2, [r3, #0]
    add r3, r0, #0x0
    add r3, #0xc
    ldrh r2, [r3, #0]
    bic r2, r1
    strh r2, [r3, #0]
    add r3, r0, #0x0
    add r3, #0xe
    ldrh r2, [r3, #0]
    bic r2, r1
    strh r2, [r3, #0]
    mov r1, #0x0
    str r1, [r0, #0x10]
    str r1, [r0, #0x14]
    str r1, [r0, #0x18]
    str r1, [r0, #0x1c]
    add r0, #0x50
    mov r1, #0x3f
    mov r2, #0x10
    blx native_fn_020042e0
    mov r0, #0x80
    blx native_fn_020038a8
    mov r0, #0x1
    lsl r0, r0, #0x8
    blx native_fn_02003950
    mov r0, #0x0
    blx native_fn_02002d00
    ldr r0, =0x04001000
    ldr r1, =0xffffe0ff
    ldr r2, [r0, #0]
    and r1, r2
    str r1, [r0, #0]
    ldr r2, [r0, #0]
    ldr r1, =0xffff1fff
    and r1, r2
    str r1, [r0, #0]
    add r0, #0x6c
    mov r1, #0x0
    blx native_fn_02002d1c
    ldr r0, =0x04001000
    ldr r1, =0xffcfffef
    ldr r2, [r0, #0]
    add r4, r0, #0x0
    and r1, r2
    mov r2, #0x10
    orr r1, r2
    str r1, [r0, #0]
    add r4, #0x8
    ldrh r3, [r4, #0]
    mov r1, #0x40
    bic r3, r1
    strh r3, [r4, #0]
    add r4, r0, #0x0
    add r4, #0xa
    ldrh r3, [r4, #0]
    bic r3, r1
    strh r3, [r4, #0]
    add r4, r0, #0x0
    add r4, #0xc
    ldrh r3, [r4, #0]
    bic r3, r1
    strh r3, [r4, #0]
    add r4, r0, #0x0
    add r4, #0xe
    ldrh r3, [r4, #0]
    bic r3, r1
    strh r3, [r4, #0]
    mov r1, #0x0
    str r1, [r0, #0x10]
    str r1, [r0, #0x14]
    str r1, [r0, #0x18]
    str r1, [r0, #0x1c]
    add r0, #0x50
    mov r1, #0x3f
    blx native_fn_020042e0
    ldr r0, =0x04000008
    mov r2, #0x3
    mov r5, #0xe1
    ldrh r1, [r0, #0]
    mov r4, #0x43
    lsl r2, r2, #0xa
    and r1, r4
    orr r1, r2
    strh r1, [r0, #0]
    ldrh r1, [r0, #0x2]
    ldr r3, =0x00000d08
    lsl r5, r5, #0x4
    and r1, r4
    orr r1, r3
    strh r1, [r0, #0x2]
    ldrh r1, [r0, #0x4]
    sub r3, #0x8
    and r1, r4
    orr r1, r5
    strh r1, [r0, #0x4]
    ldrh r1, [r0, #0x6]
    sub r5, #0x10
    add r6, r1, #0x0
    mov r1, #0xf1
    and r6, r4
    lsl r1, r1, #0x4
    orr r6, r1
    strh r6, [r0, #0x6]
    ldr r0, =0x04001008
    ldrh r6, [r0, #0]
    and r6, r4
    orr r2, r6
    strh r2, [r0, #0]
    ldrh r2, [r0, #0x2]
    and r2, r4
    orr r2, r3
    strh r2, [r0, #0x2]
    ldrh r2, [r0, #0x4]
    and r2, r4
    orr r2, r5
    strh r2, [r0, #0x4]
    ldrh r2, [r0, #0x6]
    sub r1, #0x10
    and r2, r4
    orr r1, r2
    lsl r2, r0, #0x17
    strh r1, [r0, #0x6]
    ldr r1, [r2, #0]
    ldr r0, =0xc7ffffff
    and r1, r0
    str r1, [r2, #0]
    ldr r1, [r2, #0]
    asr r0, r0, #0x3
    and r0, r1
    str r0, [r2, #0]
    ldr r2, =0x04000304
    ldr r0, =0xffff7fff
    ldrh r1, [r2, #0]
    and r0, r1
    strh r0, [r2, #0]
    bl native_fn_02203338
    bl native_fn_022042c4
    bl native_fn_022043f4
    bl native_fn_02202b84
    blx native_fn_02002c50
    ldr r2, =0x04001000
    mov r0, #0x1
    ldr r1, [r2, #0]
    lsl r0, r0, #0x10
    orr r0, r1
    str r0, [r2, #0]
    mov r0, #0x1
    blx native_fn_02002be0
    pop {r4, r5, r6, pc}
}
