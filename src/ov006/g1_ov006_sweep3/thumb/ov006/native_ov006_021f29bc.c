/* ov006 row 0x021f29bc: 144 bytes.
 *
 * What it does: 63 instructions; 8 call(s) to 0x021f2a4c, 0x02203058, 0x02202f54, +5 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x8c -> constant 0x0221c050 (image word 0x0221c050)
 *   back edge +0x3c -> +0x18
 *   test +0x3a cmp r4, #0x4
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f29bc; the literal pool and
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

extern void native_fn_021f2a4c(void);
extern void native_fn_02203058(void);
extern void native_fn_02202f54(void);
extern void native_fn_02202eb0(void);


asm u32 native_ov006_021f29bc (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    str r0, [sp]
    str r1, [sp, #0x4]
    str r2, [sp, #0x8]
    str r3, [sp, #0xc]
    mov r6, #0x6
    bl native_fn_021f2a4c
    mov r4, #0x0
    ldr r7, =0x0221c050
    add r5, r4, #0x0
ov006_021f29bc_L18:
    mov r0, #0x0
    add r1, r6, #0x0
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, [r7, #0]
    mov r2, #0x1
    str r0, [r1, r5]
    ldr r0, [r7, #0]
    mov r1, #0x0
    ldr r0, [r0, r5]
    mvn r1, r1
    bl native_fn_02202f54
    add r4, r4, #0x1
    add r5, r5, #0x4
    add r6, r6, #0x1
    cmp r4, #0x4
    blt ov006_021f29bc_L18
    ldr r0, =0x0221c050
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r2, [sp]
    ldr r0, [r0, #0]
    ldr r3, [sp, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c050
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r2, [sp, #0x4]
    ldr r0, [r0, #0x4]
    ldr r3, [sp, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c050
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r2, [sp]
    ldr r0, [r0, #0x8]
    ldr r3, [sp, #0xc]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c050
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r2, [sp, #0x4]
    ldr r0, [r0, #0xc]
    ldr r3, [sp, #0xc]
    mvn r1, r1
    bl native_fn_02202eb0
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
