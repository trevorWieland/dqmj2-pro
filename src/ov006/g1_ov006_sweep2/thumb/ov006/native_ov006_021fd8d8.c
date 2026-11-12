/* ov006 row 0x021fd8d8: 112 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x64 -> constant 0x0221c11c (image word 0x0221c11c)
 *   pool +0x68 -> constant 0xffff3be9 (image word 0xffff3be9)
 *   pool +0x6c -> native_fn_021fd828+1 (image word 0x021fd829)
 *   branch +0x0a -> +0x14
 *   branch +0x12 -> +0x62
 *   branch +0x22 -> +0x34
 *   branch +0x26 -> +0x34
 *   branch +0x32 -> +0x54
 *   branch +0x36 -> +0x3e
 *   branch +0x3c -> +0x40
 *   branch +0x46 -> +0x4a
 *   test +0x08 cmp r0, #0x0
 *   test +0x20 cmp r1, #0x0
 *   test +0x24 cmp r4, #0x0
 *   test +0x34 cmp r1, #0x0
 *   test +0x44 cmp r0, r1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd8d8; the literal pool and
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

extern void native_fn_02094398(void);
extern void native_fn_021f2be0(void);
extern void native_fn_021ff718(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_02094420(void);
extern void native_fn_021fa158(void);
extern void native_fn_021fd828(void);
extern void native_fn_021f52cc(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_021fd8d8 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r0, #0x0
    ldr r0, =0x0221c11c
    ldr r0, [r0, #0x4]
    cmp r0, #0x0
    beq ov006_021fd8d8_L14
    bl native_fn_02094398
    add r4, r0, #0x0
    beq ov006_021fd8d8_L62
ov006_021fd8d8_L14:
    bl native_fn_021f2be0
    bl native_fn_021ff718
    ldr r0, =0x0221c11c
    ldr r1, [r0, #0x4]
    cmp r1, #0x0
    beq ov006_021fd8d8_L34
    cmp r4, #0x0
    ble ov006_021fd8d8_L34
    mov r1, #0x1
    strb r1, [r0, #0]
    mov r0, #0x11
    bl native_fn_021ff6d4
    b ov006_021fd8d8_L54
ov006_021fd8d8_L34:
    cmp r1, #0x0
    beq ov006_021fd8d8_L3e
    bl native_fn_02094420
    b ov006_021fd8d8_L40
ov006_021fd8d8_L3e:
    ldr r0, =0xffff3be9
ov006_021fd8d8_L40:
    mov r1, #0x9
    mvn r1, r1
    cmp r0, r1
    blt ov006_021fd8d8_L4a
    ldr r0, =0xffff3be9
ov006_021fd8d8_L4a:
    bl native_fn_021fa158
    mov r0, #0x12
    bl native_fn_021ff6d4
ov006_021fd8d8_L54:
    ldr r0, =native_fn_021fd828+1
    bl native_fn_021f52cc
    mov r0, #0x0
    add r1, r5, #0x0
    bl native_fn_02204974
ov006_021fd8d8_L62:
    pop {r3, r4, r5, pc}
}
