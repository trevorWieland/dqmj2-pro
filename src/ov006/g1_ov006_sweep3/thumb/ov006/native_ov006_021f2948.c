/* ov006 row 0x021f2948: 116 bytes.
 *
 * What it does: 49 instructions; 6 call(s) to 0x021f2a4c, 0x02203058, 0x02202f54, +3 more; loops (back edge at +0x40); returns through pop {r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x6c -> native_data_0220b140 (image word 0x0220b140)
 *   pool +0x70 -> constant 0x0221c050 (image word 0x0221c050)
 *   back edge +0x40 -> +0x1c
 *   test +0x3e cmp r6, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2948; the literal pool and
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
extern u8 native_data_0220b140[];
extern void native_fn_02203058(void);
extern void native_fn_02202f54(void);
extern void native_fn_02202eb0(void);


asm u32 native_ov006_021f2948 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    add r4, r0, #0x0
    str r1, [sp]
    str r2, [sp, #0x4]
    str r3, [sp, #0x8]
    bl native_fn_021f2a4c
    mov r6, #0x0
    ldr r1, =native_data_0220b140
    lsl r0, r4, #0x1
    ldr r7, =0x0221c050
    add r4, r1, r0
    add r5, r6, #0x0
ov006_021f2948_L1c:
    ldrb r1, [r4, #0]
    mov r0, #0x0
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
    add r6, r6, #0x1
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r6, #0x2
    blt ov006_021f2948_L1c
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
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
