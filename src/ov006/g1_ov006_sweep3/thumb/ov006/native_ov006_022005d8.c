/* ov006 row 0x022005d8: 132 bytes.
 *
 * What it does: 52 instructions; 7 call(s) to 0x02202f98, 0x0220060c, 0x02200770, +4 more; no back edge; returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> constant 0x0221c15c (image word 0x0221c15c)
 *   pool +0x78 -> native_data_0220bade (image word 0x0220bade)
 *   pool +0x7c -> native_fn_02200730+1 (image word 0x02200731)
 *   pool +0x80 -> native_fn_0220065c+1 (image word 0x0220065d)
 *   branch +0x2a -> +0x34
 *   branch +0x42 -> +0x54
 *   branch +0x52 -> +0x62
 *   test +0x28 cmp r0, r1
 *   test +0x40 cmp r0, #0x5
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022005d8; the literal pool and
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

extern void native_fn_02202f98(void);
extern u8 native_data_0220bade[];
extern void native_fn_02200770(void);
extern void native_fn_02200730(void);
extern void native_fn_0220490c(void);
extern void native_fn_0220065c(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_022005d8 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c15c
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r2, sp, #0x4
    ldr r0, [r0, #0]
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r0, [sp]
    ldr r1, =0x0221c15c
    sub r0, #0xc
    ldr r1, [r1, #0]
    str r0, [sp]
    ldrb r1, [r1, #0x1c]
    lsl r2, r1, #0x2
    ldr r1, =native_data_0220bade
    ldrh r1, [r1, r2]
    cmp r0, r1
    ble ov006_022005d8_L34
    bl native_fn_02200770
    add sp, #0x8
    pop {r4, pc}
ov006_022005d8_L34:
    add r0, r1, #0x0
    bl native_fn_02200770
    ldr r0, =0x0221c15c
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x1c]
    cmp r0, #0x5
    bne ov006_022005d8_L54
    mov r0, #0x0
    ldr r1, =native_fn_02200730+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c15c
    b ov006_022005d8_L62
ov006_022005d8_L54:
    mov r0, #0x0
    ldr r1, =native_fn_0220065c+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c15c
ov006_022005d8_L62:
    ldr r1, [r1, #0]
    str r0, [r1, #0x14]
    mov r0, #0x1
    add r1, r4, #0x0
    bl native_fn_02204974
    add sp, #0x8
    pop {r4, pc}
    mov r8, r8
}
