/* ov006 row 0x021ff734: 184 bytes.
 *
 * What it does: 74 instructions; 9 call(s) to 0x02203c08, 0x02203058, 0x02202f54, +6 more; loops (back edge at +0x7e); returns through pop {r3, r4, r5, r6, r7, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa4 -> constant 0x0221c150 (image word 0x0221c150)
 *   pool +0xa8 -> native_data_0220ba12 (image word 0x0220ba12)
 *   pool +0xac -> native_data_0220b9f4 (image word 0x0220b9f4)
 *   pool +0xb0 -> native_data_0220ba03 (image word 0x0220ba03)
 *   pool +0xb4 -> native_fn_021ff7ec+1 (image word 0x021ff7ed)
 *   back edge +0x7e -> +0x28
 *   test +0x7c cmp r0, #0x5
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff734; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data_0220ba12[];
extern u8 native_data_0220b9f4[];
extern u8 native_data_0220ba03[];
extern void native_fn_02203058(void);
extern void native_fn_02202f54(void);
extern void native_fn_02202eb0(void);
extern void native_fn_02202e50(void);
extern void native_fn_021ff7ec(void);
extern void native_fn_0220490c(void);
extern void native_fn_021ffdf4(void);
extern void native_fn_021ff6d4(void);


asm u32 native_ov006_021ff734 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    str r0, [sp]
    mov r0, #0x1c
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =0x0221c150
    ldr r6, =native_data_0220ba12
    str r0, [r1, #0x4]
    mov r0, #0x0
    str r0, [sp, #0x4]
    ldr r0, [sp]
    ldr r4, [sp, #0x4]
    lsl r1, r0, #0x2
    add r1, r0, r1
    ldr r0, =native_data_0220b9f4
    add r7, r0, r1
    ldr r0, =native_data_0220ba03
    add r5, r0, r1
ov006_021ff734_L28:
    ldrb r1, [r7, #0]
    mov r0, #0x1
    add r2, r0, #0x0
    bl native_fn_02203058
    ldr r1, =0x0221c150
    mov r2, #0x0
    ldr r1, [r1, #0x4]
    str r0, [r1, r4]
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    ldr r0, [r0, r4]
    bl native_fn_02202f54
    ldr r0, =0x0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    mvn r1, r1
    add r2, r1, #0x0
    ldrh r3, [r6, #0x2]
    ldr r0, [r0, r4]
    sub r2, #0x29
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
    add r7, r7, #0x1
    add r0, r0, #0x1
    add r4, r4, #0x4
    add r6, r6, #0x4
    add r5, r5, #0x1
    str r0, [sp, #0x4]
    cmp r0, #0x5
    blt ov006_021ff734_L28
    mov r0, #0x0
    ldr r1, =native_fn_021ff7ec+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c150
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x14]
    ldr r0, [sp]
    bl native_fn_021ffdf4
    mov r0, #0xd
    bl native_fn_021ff6d4
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
