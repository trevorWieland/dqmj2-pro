/* ov006 row 0x021f43ac: 88 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x4c -> constant 0x0221c060 (image word 0x0221c060)
 *   pool +0x50 -> constant 0x01ff0000 (image word 0x01ff0000)
 *   pool +0x54 -> native_fn_021f4404+1 (image word 0x021f4405)
 *   branch +0x22 -> +0x2e
 *   test +0x20 cmp r1, #0x91
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f43ac; the literal pool and
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

extern void native_fn_021f4944(void);
extern void native_fn_021f4404(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021f43ac (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c060
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x34]
    ldr r1, [r0, #0]
    ldr r0, =0x01ff0000
    and r0, r1
    lsr r0, r0, #0x10
    str r0, [sp, #0x4]
    lsl r0, r1, #0x18
    lsr r1, r0, #0x18
    str r1, [sp]
    sub r1, #0xc
    str r1, [sp]
    cmp r1, #0x91
    ble ov006_021f43ac_L2e
    mov r0, #0x3
    bl native_fn_021f4944
    add sp, #0x8
    pop {r4, pc}
ov006_021f43ac_L2e:
    mov r0, #0x3
    mov r1, #0x91
    bl native_fn_021f4944
    mov r0, #0x4
    mov r1, #0xc0
    bl native_fn_021f4944
    ldr r1, =native_fn_021f4404+1
    add r0, r4, #0x0
    bl native_fn_02204970
    add sp, #0x8
    pop {r4, pc}
    mov r8, r8
}
