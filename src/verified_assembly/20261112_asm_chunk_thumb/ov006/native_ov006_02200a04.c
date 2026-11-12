/* ov006 row 0x02200a04: 120 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x68 -> constant 0xffff1fff (image word 0xffff1fff)
 *   pool +0x6c -> native_data3_0221c15c (image word 0x0221c15c)
 *   pool +0x70 -> native_data_0220bb3c (image word 0x0220bb3c)
 *   pool +0x74 -> native_data4_0221c15c (image word 0x0221c15c)
 *   branch +0x32 -> +0x50
 *   branch +0x3c -> +0x42
 *   back edge +0x4e -> +0x36
 *   test +0x30 cmp r1, #0x0
 *   test +0x3a cmp r0, #0x0
 *   test +0x4c cmp r4, r1
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200a04; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 120 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data3_0221c15c[];
extern void native_fn_02202d64(void);
extern u8 native_data_0220bb3c[];
extern void native_fn_022034bc(void);
extern void native_fn_02204974(void);
extern u8 native_data4_0221c15c[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_02200a04 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r2, #0x1
    lsl r2, r2, #0x1a
    str r0, [sp]
    ldr r1, [r2, #0]
    ldr r0, =0xffff1fff
    and r0, r1
    str r0, [r2, #0]
    ldr r0, =native_data3_0221c15c
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_02202d64
    ldr r0, =native_data3_0221c15c
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x4]
    bl native_fn_02202d64
    ldr r7, =native_data3_0221c15c
    ldr r6, =native_data_0220bb3c
    ldr r0, [r7, #0]
    mov r4, #0x0
    ldrb r1, [r0, #0x1c]
    ldrb r1, [r6, r1]
    cmp r1, #0x0
    ble ov006_02200a04_L50
    add r5, r4, #0x0
ov006_02200a04_L36:
    add r0, r0, r5
    ldr r0, [r0, #0x8]
    cmp r0, #0x0
    beq ov006_02200a04_L42
    bl native_fn_02202d64
ov006_02200a04_L42:
    ldr r0, [r7, #0]
    add r4, r4, #0x1
    ldrb r1, [r0, #0x1c]
    add r5, r5, #0x4
    ldrb r1, [r6, r1]
    cmp r4, r1
    blt ov006_02200a04_L36
ov006_02200a04_L50:
    ldr r0, [r0, #0x10]
    bl native_fn_022034bc
    ldr r1, [sp]
    mov r0, #0x1
    bl native_fn_02204974
    ldr r0, =native_data4_0221c15c
    bl native_fn_02203c20
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
