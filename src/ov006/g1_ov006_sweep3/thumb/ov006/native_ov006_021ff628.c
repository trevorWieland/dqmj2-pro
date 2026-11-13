/* ov006 row 0x021ff628: 140 bytes.
 *
 * What it does: 54 instructions; 11 call(s) to 0x02203c08, 0x02202a80, 0x02037dc8, +8 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x80 -> constant 0x0221c14c (image word 0x0221c14c)
 *   pool +0x84 -> native_data_0220e1cc (image word 0x0220e1cc)
 *   pool +0x88 -> native_fn_021ff72c+1 (image word 0x021ff72d)
 *   back edge +0x66 -> +0x4a
 *   test +0x64 cmp r5, #0x20
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ff628; the literal pool and
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
extern u8 native_data_0220e1cc[];
extern void native_fn_02202a80(void);
extern void native_fn_02037dc8(void);
extern void native_fn_02038c9c(void);
extern void native_fn_02039a14(void);
extern void native_fn_020380f4(void);
extern void native_fn_02037ff0(void);
extern void native_fn_02038008(void);
extern void native_fn_02038028(void);
extern void native_fn_021ff72c(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021ff628 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r0, #0xa0
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =0x0221c14c
    mov r2, #0x20
    str r0, [r1, #0]
    ldr r0, =native_data_0220e1cc
    add r1, sp, #0x0
    bl native_fn_02202a80
    ldr r1, =0x0221c14c
    ldr r1, [r1, #0]
    add r1, #0x98
    str r0, [r1, #0]
    blx native_fn_02037dc8
    ldr r0, =0x0221c14c
    ldr r0, [r0, #0]
    add r1, r0, #0x0
    add r1, #0x98
    ldr r1, [r1, #0]
    blx native_fn_02038c9c
    mov r0, #0x0
    blx native_fn_02039a14
    ldr r0, =0x0221c14c
    ldr r0, [r0, #0]
    add r0, #0x94
    blx native_fn_020380f4
    mov r5, #0x0
    mov r4, #0x7f
    mov r6, #0x1
    add r7, r5, #0x0
ov006_021ff628_L4a:
    add r0, r5, #0x0
    add r1, r4, #0x0
    blx native_fn_02037ff0
    add r0, r5, #0x0
    add r1, r6, #0x0
    blx native_fn_02038008
    add r0, r5, #0x0
    add r1, r7, #0x0
    blx native_fn_02038028
    add r5, r5, #0x1
    cmp r5, #0x20
    blt ov006_021ff628_L4a
    mov r0, #0x0
    ldr r1, =native_fn_021ff72c+1
    add r2, r0, #0x0
    mov r3, #0xc8
    bl native_fn_0220490c
    ldr r1, =0x0221c14c
    ldr r1, [r1, #0]
    add r1, #0x9c
    str r0, [r1, #0]
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
