/* ov006 row 0x021f3108: 96 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x54 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x58 -> constant 0x0000011d (image word 0x0000011d)
 *   pool +0x5c -> native_fn_021f3168+1 (image word 0x021f3169)
 *   branch +0x20 -> +0x34
 *   test +0x1e cmp r2, #0xaa
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3108; the literal pool and
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

extern void native_fn_02202f98(void);
extern void native_fn_021f37f0(void);
extern void native_fn_021f3a78(void);
extern void native_fn_021f3168(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f3108 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c05c
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r2, sp, #0x4
    add r0, #0xfc
    ldr r0, [r0, #0]
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r2, [sp]
    sub r2, #0xc
    str r2, [sp]
    cmp r2, #0xaa
    ble ov006_021f3108_L34
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011d
    ldrb r0, [r1, r0]
    mov r1, #0x4
    bl native_fn_021f37f0
    add sp, #0x8
    pop {r4, pc}
ov006_021f3108_L34:
    ldr r0, =0x0221c05c
    mov r2, #0xaa
    ldr r1, [r0, #0]
    ldr r0, =0x0000011d
    ldrb r0, [r1, r0]
    mov r1, #0x4
    bl native_fn_021f37f0
    bl native_fn_021f3a78
    ldr r1, =native_fn_021f3168+1
    add r0, r4, #0x0
    bl native_fn_02204970
    add sp, #0x8
    pop {r4, pc}
}
