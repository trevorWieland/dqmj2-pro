/* ov006 row 0x021fe60c: 132 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x78 -> constant 0x0221c140 (image word 0x0221c140)
 *   pool +0x7c -> native_data_0220b998 (image word 0x0220b998)
 *   pool +0x80 -> native_fn_021fe6f8+1 (image word 0x021fe6f9)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fe60c; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern void native_fn_022038d0(void);
extern u8 native_data_0220b998[];
extern void native_fn_02203058(void);
extern void native_fn_02202eb0(void);
extern void native_fn_02202f54(void);
extern void native_fn_021fe6f8(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021fe60c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    add r6, r1, #0x0
    mov r0, #0x20
    mov r1, #0x4
    add r7, r2, #0x0
    add r4, r3, #0x0
    bl ov006_clear_buffer_02203c08
    ldr r2, =0x0221c140
    ldr r1, [sp, #0x18]
    str r0, [r2, #0]
    strb r5, [r0, #0x1b]
    ldr r0, [r2, #0]
    strb r6, [r0, #0x19]
    ldr r0, [r2, #0]
    strb r1, [r0, #0x1a]
    ldr r2, [r2, #0]
    add r0, r7, #0x0
    add r1, r4, #0x0
    add r2, #0x10
    bl native_fn_022038d0
    ldr r1, =native_data_0220b998
    mov r0, #0x0
    ldrb r1, [r1, r5]
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, =0x0221c140
    ldr r3, [sp, #0x18]
    ldr r2, [r1, #0]
    add r3, r4, r3
    str r0, [r2, #0]
    ldr r0, [r1, #0]
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    add r2, r7, #0x0
    bl native_fn_02202eb0
    ldr r0, =0x0221c140
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, #0]
    mov r2, #0x1
    bl native_fn_02202f54
    mov r0, #0x0
    ldr r1, =native_fn_021fe6f8+1
    add r2, r0, #0x0
    mov r3, #0x80
    bl native_fn_0220490c
    ldr r1, =0x0221c140
    ldr r1, [r1, #0]
    str r0, [r1, #0xc]
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
