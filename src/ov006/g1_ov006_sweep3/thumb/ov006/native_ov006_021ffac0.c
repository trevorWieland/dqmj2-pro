/* ov006 row 0x021ffac0: 144 bytes.
 *
 * What it does: 58 instructions; 7 call(s) to 0x02202dc0, 0x02202ff0, 0x02202f54, +4 more; loops (back edge at +0x72); returns through pop {r3, r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x80 -> native_data_0220b9f4 (image word 0x0220b9f4)
 *   pool +0x84 -> native_data_0220ba03 (image word 0x0220ba03)
 *   pool +0x88 -> native_data_0220ba12 (image word 0x0220ba12)
 *   pool +0x8c -> constant 0x0221c150 (image word 0x0221c150)
 *   back edge +0x72 -> +0x18
 *   test +0x70 cmp r0, #0x5
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ffac0; the literal pool and
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

extern u8 native_data_0220b9f4[];
extern u8 native_data_0220ba03[];
extern u8 native_data_0220ba12[];
extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);
extern void native_fn_02202f54(void);
extern void native_fn_02202eb0(void);
extern void native_fn_02202e50(void);
extern void native_fn_021ffdf4(void);


asm u32 native_ov006_021ffac0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    lsl r1, r0, #0x2
    str r0, [sp]
    add r1, r0, r1
    ldr r0, =native_data_0220b9f4
    mov r4, #0x0
    add r7, r0, r1
    ldr r0, =native_data_0220ba03
    ldr r6, =native_data_0220ba12
    str r4, [sp, #0x4]
    add r5, r0, r1
ov006_021ffac0_L18:
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    ldr r0, [r0, r4]
    bl native_fn_02202dc0
    add r2, r0, #0x0
    ldrb r1, [r7, #0]
    mov r0, #0x1
    bl native_fn_02202ff0
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    ldr r0, [r0, r4]
    mov r2, #0x0
    bl native_fn_02202f54
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    ldrh r2, [r6, #0]
    ldrh r3, [r6, #0x2]
    ldr r0, [r0, r4]
    mvn r1, r1
    bl native_fn_02202eb0
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    ldrb r3, [r5, #0]
    ldr r0, [r0, r4]
    mvn r1, r1
    mov r2, #0x0
    bl native_fn_02202e50
    ldr r0, [sp, #0x4]
    add r4, #0x8
    add r0, r0, #0x2
    add r7, r7, #0x2
    add r6, #0x8
    add r5, r5, #0x2
    str r0, [sp, #0x4]
    cmp r0, #0x5
    blt ov006_021ffac0_L18
    ldr r0, [sp]
    bl native_fn_021ffdf4
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
