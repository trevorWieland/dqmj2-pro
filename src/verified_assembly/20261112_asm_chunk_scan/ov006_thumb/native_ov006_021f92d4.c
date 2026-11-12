/* ov006 row 0x021f92d4: 64 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x38 -> native_data_0221c0e0 (image word 0x0221c0e0)
 *   pool +0x3c -> native_fn_021f9314+1 (image word 0x021f9315)
 *   branch +0x16 -> +0x1e
 *   branch +0x1a -> +0x26
 *   branch +0x24 -> +0x2c
 *   test +0x14 cmp r0, #0x0
 *   test +0x18 cmp r0, #0x1
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f92d4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02200574(void);
extern u8 native_data_0221c0e0[];
extern void native_fn_021ff6d4(void);
extern void native_fn_02200548(void);
extern void native_fn_021f9314(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f92d4 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_02200574
    ldr r1, =native_data_0221c0e0
    ldr r2, [r1, #0]
    add r2, #0x2a
    strb r0, [r2, #0]
    ldr r0, [r1, #0]
    add r0, #0x2a
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f92d4_L1e
    cmp r0, #0x1
    beq ov006_021f92d4_L26
    pop {r3, pc}
ov006_021f92d4_L1e:
    mov r0, #0x7
    bl native_fn_021ff6d4
    b ov006_021f92d4_L2c
ov006_021f92d4_L26:
    mov r0, #0xe
    bl native_fn_021ff6d4
ov006_021f92d4_L2c:
    bl native_fn_02200548
    ldr r0, =native_fn_021f9314+1
    bl native_fn_021f52cc
    pop {r3, pc}
}
