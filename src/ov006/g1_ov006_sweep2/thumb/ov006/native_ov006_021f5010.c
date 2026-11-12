/* ov006 row 0x021f5010: 160 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x90 -> constant 0x04000208 (image word 0x04000208)
 *   pool +0x94 -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x98 -> constant 0xfffeffff (image word 0xfffeffff)
 *   pool +0x9c -> constant 0x0221c06c (image word 0x0221c06c)
 *   branch +0x1e -> +0x24
 *   branch +0x2a -> +0x30
 *   test +0x1c cmp r0, #0x0
 *   test +0x28 cmp r0, #0x0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5010; the literal pool and
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

extern void native_fn_02002c14(void);
extern void native_fn_02007a24(void);
extern void native_fn_02008430(void);
extern void native_fn_02007c58(void);
extern void native_fn_02002be0(void);
extern void native_fn_02002a90(void);
extern void native_fn_0200bcdc(void);
extern void native_fn_0200dbc0(void);
extern void native_fn_0200f304(void);
extern void native_fn_02204608(void);
extern void native_fn_02203b94(void);
extern void native_fn_022041a0(void);
extern void native_fn_022047d4(void);
extern void native_fn_02202894(void);
extern void native_fn_02203c74(void);
extern void native_fn_02203148(void);
extern void ov006_clear_buffer_02203c08(void);
extern void native_fn_020a4e70(void);
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f5010 (register u32 a0)
{
    push {r3, lr}
    ldr r1, =0x04000208
    ldrh r0, [r1, #0]
    mov r0, #0x0
    strh r0, [r1, #0]
    blx native_fn_02002c14
    ldr r2, =0x04001000
    ldr r0, =0xfffeffff
    ldr r1, [r2, #0]
    and r0, r1
    str r0, [r2, #0]
    blx native_fn_02007a24
    cmp r0, #0x0
    bne ov006_021f5010_L24
    blx native_fn_02008430
ov006_021f5010_L24:
    blx native_fn_02007c58
    cmp r0, #0x0
    bne ov006_021f5010_L30
    blx native_fn_02008430
ov006_021f5010_L30:
    mov r0, #0x0
    blx native_fn_02002be0
    blx native_fn_02002a90
    mov r0, #0x0
    mvn r0, r0
    blx native_fn_0200bcdc
    blx native_fn_0200dbc0
    blx native_fn_0200f304
    blx native_fn_02002c14
    ldr r2, =0x04001000
    ldr r0, =0xfffeffff
    ldr r1, [r2, #0]
    and r0, r1
    str r0, [r2, #0]
    bl native_fn_02204608
    ldr r0, =0x0221c06c
    ldr r0, [r0, #0x4]
    bl native_fn_02203b94
    bl native_fn_022041a0
    bl native_fn_022047d4
    bl native_fn_02202894
    bl native_fn_02203c74
    bl native_fn_02203148
    mov r0, #0x7
    lsl r0, r0, #0x8
    mov r1, #0x20
    bl ov006_clear_buffer_02203c08
    str r0, [sp]
    bl native_fn_020a4e70
    add r0, sp, #0x0
    bl native_fn_02203c20
    pop {r3, pc}
}
