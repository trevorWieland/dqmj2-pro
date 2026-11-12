/* ov006 row 0x021f4d90: 132 bytes.
 *
 * What it does: 55 instructions; 11 call(s) to 0x02204974, 0x02202d64, 0x022034bc, +8 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> native_data_0221c060 (image word 0x0221c060)
 *   pool +0x80 -> native_data2_0221c060 (image word 0x0221c060)
 *   back edge +0x28 -> +0x10
 *   back edge +0x40 -> +0x30
 *   back edge +0x58 -> +0x48
 *   back edge +0x70 -> +0x60
 *   test +0x26 cmp r4, #0x4
 *   test +0x3e cmp r5, #0x2
 *   test +0x56 cmp r5, #0x2
 *   test +0x6e cmp r5, #0xa
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4d90; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02204974(void);
extern u8 native_data_0221c060[];
extern void native_fn_02202d64(void);
extern void native_fn_022034bc(void);
extern void native_fn_022043a4(void);
extern u8 native_data2_0221c060[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f4d90 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r1, r0, #0x0
    mov r0, #0x0
    bl native_fn_02204974
    mov r4, #0x0
    ldr r6, =native_data_0221c060
    add r5, r4, #0x0
ov006_021f4d90_L10:
    ldr r0, [r6, #0]
    add r0, r0, r5
    ldr r0, [r0, #0x48]
    bl native_fn_02202d64
    ldr r0, [r6, #0]
    ldr r0, [r0, r5]
    bl native_fn_022034bc
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x4
    blt ov006_021f4d90_L10
    mov r5, #0x0
    ldr r6, =native_data_0221c060
    add r4, r5, #0x0
ov006_021f4d90_L30:
    ldr r0, [r6, #0]
    add r0, r0, r4
    ldr r0, [r0, #0x40]
    bl native_fn_02202d64
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f4d90_L30
    mov r5, #0x0
    ldr r6, =native_data_0221c060
    add r4, r5, #0x0
ov006_021f4d90_L48:
    ldr r0, [r6, #0]
    add r0, r0, r4
    ldr r0, [r0, #0x38]
    bl native_fn_022043a4
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f4d90_L48
    mov r5, #0x0
    ldr r6, =native_data_0221c060
    add r4, r5, #0x0
ov006_021f4d90_L60:
    ldr r0, [r6, #0]
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    bl native_fn_022043a4
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0xa
    blt ov006_021f4d90_L60
    ldr r0, =native_data2_0221c060
    bl native_fn_02203c20
    pop {r4, r5, r6, pc}
    mov r8, r8
}
