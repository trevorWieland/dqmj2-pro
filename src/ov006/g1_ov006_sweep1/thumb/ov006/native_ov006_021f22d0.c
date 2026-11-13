/* ov006 row 0x021f22d0: 160 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x90 -> native_data_0220b0e8 (image word 0x0220b0e8)
 *   pool +0x94 -> native_data6_0221c008 (image word 0x0221c008)
 *   pool +0x98 -> native_data_0220b0cc (image word 0x0220b0cc)
 *   pool +0x9c -> native_fn_021f2464+1 (image word 0x021f2465)
 *   branch +0x24 -> +0x58
 *   back edge +0x56 -> +0x2e
 *   test +0x1e cmp r7, #0x0
 *   test +0x54 cmp r6, r7
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f22d0; the literal pool and
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

extern u8 native_data_0220b0e8[];
extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data6_0221c008[];
extern u8 native_data_0220b0cc[];
extern void native_fn_02203058(void);
extern void native_fn_02202f54(void);
extern void native_fn_021f2404(void);
extern void native_fn_021f2464(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021f22d0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r4, r0, #0x0
    ldr r0, =native_data_0220b0e8
    mov r1, #0x4
    ldrb r7, [r0, r4]
    mov r0, #0x1c
    bl ov006_clear_buffer_02203c08
    ldr r1, =native_data6_0221c008
    mov r6, #0x0
    str r0, [r1, #0]
    mov r1, #0x1
    mvn r1, r1
    strb r1, [r0, #0x16]
    ldr r0, =native_data6_0221c008
    cmp r7, #0x0
    ldr r0, [r0, #0]
    strb r4, [r0, #0x17]
    ble ov006_021f22d0_L58
    ldr r1, =native_data_0220b0cc
    lsl r0, r4, #0x1
    add r4, r1, r0
    add r5, r6, #0x0
ov006_021f22d0_L2e:
    ldrb r1, [r4, #0]
    mov r0, #0x0
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, =native_data6_0221c008
    mov r2, #0x1
    ldr r1, [r1, #0]
    str r0, [r1, r5]
    ldr r0, =native_data6_0221c008
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, r5]
    bl native_fn_02202f54
    add r6, r6, #0x1
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r6, r7
    blt ov006_021f22d0_L2e
ov006_021f22d0_L58:
    mov r1, #0x1
    mov r0, #0x0
    add r2, r1, #0x0
    bl native_fn_02203058
    ldr r1, =native_data6_0221c008
    ldr r2, [r1, #0]
    str r0, [r2, #0x8]
    ldr r0, [r1, #0]
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    mvn r1, r1
    mov r2, #0x1
    bl native_fn_02202f54
    mov r0, #0xc0
    bl native_fn_021f2404
    mov r0, #0x0
    ldr r1, =native_fn_021f2464+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data6_0221c008
    ldr r1, [r1, #0]
    str r0, [r1, #0xc]
    pop {r3, r4, r5, r6, r7, pc}
}
