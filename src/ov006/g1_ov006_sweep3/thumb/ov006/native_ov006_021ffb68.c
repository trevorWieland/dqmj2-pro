/* ov006 row 0x021ffb68: 92 bytes.
 *
 * What it does: 38 instructions; 5 call(s) to 0x02202f98, 0x021ffb9c, 0x02202eb0, +2 more; no back edge; returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x54 -> constant 0x0221c150 (image word 0x0221c150)
 *   pool +0x58 -> native_fn_021ffbc4+1 (image word 0x021ffbc5)
 *   branch +0x1e -> +0x34
 *   test +0x1c cmp r2, #0x98
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ffb68; the literal pool and
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
extern void native_fn_02202eb0(void);
extern void native_fn_021ffbc4(void);
extern void native_fn_02204970(void);


asm u32 native_ov006_021ffb68 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r2, sp, #0x4
    ldr r0, [r0, #0x10]
    add r3, sp, #0x0
    bl native_fn_02202f98
    ldr r2, [sp, #0x4]
    sub r2, #0x8
    str r2, [sp, #0x4]
    cmp r2, #0x98
    ble ov006_021ffb68_L34
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    ldr r0, [r0, #0x10]
    mov r3, #0x21
    bl native_fn_02202eb0
    add sp, #0x8
    pop {r4, pc}
ov006_021ffb68_L34:
    ldr r0, =0x0221c150
    mov r2, #0x98
    ldr r0, [r0, #0x4]
    str r2, [sp, #0x4]
    add r1, r2, #0x0
    ldr r0, [r0, #0x10]
    sub r1, #0x99
    mov r3, #0x21
    bl native_fn_02202eb0
    ldr r1, =native_fn_021ffbc4+1
    add r0, r4, #0x0
    bl native_fn_02204970
    add sp, #0x8
    pop {r4, pc}
}
