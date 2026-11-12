/* ov006 row 0x021f24d4: 244 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd4 -> native_data7_0221c008 (image word 0x0221c008)
 *   pool +0xd8 -> native_data_0220b0e8 (image word 0x0220b0e8)
 *   pool +0xdc -> native_data2_0220b0c4 (image word 0x0220b0c4)
 *   pool +0xe0 -> native_data2_0220b0da (image word 0x0220b0da)
 *   pool +0xe4 -> native_data_0220b0c0 (image word 0x0220b0c0)
 *   pool +0xe8 -> native_data_0220b0cc (image word 0x0220b0cc)
 *   pool +0xec -> native_data_0220b0c6 (image word 0x0220b0c6)
 *   pool +0xf0 -> native_fn_021f2654+1 (image word 0x021f2655)
 *   branch +0x12 -> +0xc6
 *   branch +0x1c -> +0xd0
 *   branch +0x22 -> +0xc6
 *   branch +0x4a -> +0xc0
 *   branch +0x54 -> +0xc6
 *   back edge +0xc4 -> +0x28
 *   test +0x10 cmp r0, #0x0
 *   test +0x1a cmp r1, r0
 *   test +0x20 cmp r4, #0x0
 *   test +0x48 cmp r0, #0x0
 *   test +0x52 cmp r1, #0x0
 *   test +0xc2 cmp r5, r4
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f24d4; the literal pool and
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

extern u8 native_data7_0221c008[];
extern u8 native_data_0220b0e8[];
extern u8 native_data2_0220b0c4[];
extern u8 native_data2_0220b0da[];
extern u8 native_data_0220b0c0[];
extern void native_fn_022038e8(void);
extern void native_fn_02203fac(void);
extern u8 native_data_0220b0cc[];
extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);
extern u8 native_data_0220b0c6[];
extern void native_fn_02202eb0(void);
extern void native_fn_02202f54(void);
extern void native_fn_021f2654(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f24d4 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =native_data7_0221c008
    ldr r2, [r0, #0]
    ldr r0, =native_data_0220b0e8
    ldrb r1, [r2, #0x17]
    ldrb r4, [r0, r1]
    ldrb r0, [r2, #0x18]
    cmp r0, #0x0
    bne ov006_021f24d4_Lc6
    mov r0, #0x16
    ldrsb r1, [r2, r0]
    sub r0, #0x17
    cmp r1, r0
    bne ov006_021f24d4_Ld0
    mov r5, #0x0
    cmp r4, #0x0
    ble ov006_021f24d4_Lc6
    ldr r7, =native_data2_0220b0c4
    add r6, sp, #0x0
ov006_021f24d4_L28:
    ldr r0, =native_data7_0221c008
    add r2, r6, #0x0
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x17]
    lsl r1, r0, #0x1
    ldr r0, =native_data2_0220b0da
    add r0, r0, r1
    ldrb r0, [r5, r0]
    ldr r1, =native_data_0220b0c0
    lsl r0, r0, #0x2
    add r0, r7, r0
    bl native_fn_022038e8
    add r0, r6, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f24d4_Lc0
    ldr r0, =native_data7_0221c008
    ldr r0, [r0, #0]
    ldr r1, [r0, #0x10]
    cmp r1, #0x0
    bne ov006_021f24d4_Lc6
    ldrb r1, [r0, #0x17]
    lsl r4, r5, #0x2
    ldr r0, [r0, r4]
    lsl r2, r1, #0x1
    ldr r1, =native_data_0220b0cc
    add r1, r1, r2
    ldrb r6, [r5, r1]
    mov r1, #0x0
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    add r1, r6, #0x1
    bl native_fn_02202ff0
    ldr r0, =native_data7_0221c008
    ldr r6, =native_data_0220b0c6
    ldr r0, [r0, #0]
    ldrb r1, [r0, #0x17]
    ldr r0, [r0, r4]
    lsl r2, r1, #0x1
    ldr r1, =native_data2_0220b0da
    add r1, r1, r2
    ldrb r1, [r5, r1]
    ldr r2, =native_data2_0220b0c4
    lsl r3, r1, #0x2
    ldrh r2, [r2, r3]
    mov r1, #0x0
    ldrh r3, [r6, r3]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =native_data7_0221c008
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, r4]
    mov r2, #0x1
    bl native_fn_02202f54
    mov r0, #0x0
    ldr r1, =native_fn_021f2654+1
    add r2, r0, #0x0
    mov r3, #0x6e
    bl native_fn_0220490c
    ldr r1, =native_data7_0221c008
    add sp, #0x8
    ldr r2, [r1, #0]
    str r0, [r2, #0x10]
    ldr r0, [r1, #0]
    strb r5, [r0, #0x16]
    pop {r3, r4, r5, r6, r7, pc}
ov006_021f24d4_Lc0:
    add r5, r5, #0x1
    cmp r5, r4
    blt ov006_021f24d4_L28
ov006_021f24d4_Lc6:
    ldr r0, =native_data7_0221c008
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    strb r1, [r0, #0x16]
ov006_021f24d4_Ld0:
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
