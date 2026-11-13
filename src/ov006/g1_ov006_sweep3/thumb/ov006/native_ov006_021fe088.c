/* ov006 row 0x021fe088: 108 bytes.
 *
 * What it does: 37 instructions; 11 call(s) to 0x021fe0f4, 0x021f2ad4, 0x021f27fc, +8 more; loops (back edge at +0x10); returns through pop {pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x60 -> constant 0x0221c130 (image word 0x0221c130)
 *   pool +0x64 -> native_fn_021fe338+1 (image word 0x021fe339)
 *   pool +0x68 -> native_fn_021fe164+1 (image word 0x021fe165)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fe088; the literal pool and
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

extern void native_fn_021fe0f4(void);
extern void native_fn_021f2ad4(void);
extern void native_fn_021f27fc(void);
extern void native_fn_02008218(void);
extern void native_fn_02008be0(void);
extern void native_fn_02008bf8(void);
extern void native_fn_021f2890(void);
extern void native_fn_021f218c(void);
extern void native_fn_021fe338(void);
extern void native_fn_021ffe5c(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021fe164(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021fe088 (register u32 a0)
{
    push {lr}
    sub sp, #0x6c
    ldr r0, =0x0221c130
    mov r1, #0x0
    strb r1, [r0, #0]
    bl native_fn_021fe0f4
    mov r0, #0x8
    bl native_fn_021f2ad4
    mov r0, #0x2
    bl native_fn_021f27fc
    add r0, sp, #0x14
    add r0, #0x2
    blx native_fn_02008218
    mov r0, #0x0
    add r1, sp, #0x0
    mov r2, #0x16
    blx native_fn_02008be0
    add r2, sp, #0x0
    ldrh r2, [r2, #0x30]
    add r0, sp, #0x18
    add r0, #0x2
    add r1, sp, #0x0
    lsl r2, r2, #0x1
    blx native_fn_02008bf8
    add r0, sp, #0x0
    mov r1, #0x28
    bl native_fn_021f2890
    mov r0, #0x0
    bl native_fn_021f218c
    ldr r0, =native_fn_021fe338+1
    bl native_fn_021ffe5c
    mov r0, #0xb
    bl native_fn_021ff6d4
    ldr r0, =native_fn_021fe164+1
    bl ov006_main_loop_set_callback_021f52cc
    add sp, #0x6c
    pop {pc}
}
