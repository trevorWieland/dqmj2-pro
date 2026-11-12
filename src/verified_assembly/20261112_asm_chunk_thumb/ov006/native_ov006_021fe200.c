/* ov006 row 0x021fe200: 52 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> native_data2_0221c130 (image word 0x0221c130)
 *   pool +0x30 -> native_fn_021fe234+1 (image word 0x021fe235)
 *   branch +0x08 -> +0x28
 *   branch +0x10 -> +0x28
 *   test +0x06 cmp r0, #0x0
 *   test +0x0e cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fe200; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0221c130[];
extern void native_fn_021f2390(void);
extern void native_fn_021ff718(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021fe234(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021fe200 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =native_data2_0221c130
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021fe200_L28
    bl native_fn_021f2390
    cmp r0, #0x0
    bne ov006_021fe200_L28
    ldr r0, =native_data2_0221c130
    mov r1, #0x2
    strb r1, [r0, #0]
    bl native_fn_021ff718
    mov r0, #0x7
    bl native_fn_021ff6d4
    ldr r0, =native_fn_021fe234+1
    bl native_fn_021f52cc
ov006_021fe200_L28:
    pop {r3, pc}
    mov r8, r8
}
