/* ov000 row 0x0222a768: 172 bytes.
 *
 * What it does: 39 instructions; 8 call(s) to 0x02004120, 0x02008c58, 0x02004174, +5 more; loops (back edge at +0x04); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x9c -> constant 0x022475ec (image word 0x022475ec)
 *   pool +0xa0 -> constant 0x022475fc (image word 0x022475fc)
 *   pool +0xa4 -> constant 0x022475d4 (image word 0x022475d4)
 *   pool +0xa8 -> constant 0x022475dc (image word 0x022475dc)
 *   back edge +0x94 -> +0x7c
 *   test +0x54 cmp r1, #8
 *   test +0x70 cmp r12, #0
 *   test +0x90 cmp r3, r12
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222a768; the literal pool and
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

extern void native_fn_02004120(void);
extern void native_fn_02008c58(void);
extern void native_fn_02004174(void);
extern void native_fn_02048e74(void);
extern void native_fn_02048fcc(void);
extern void native_fn_02063b18(void);


asm u32 native_ov000_0222a768 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02004120
    mov r1, r0
    mov r0, #0
    mov r2, #32768
    bl native_fn_02008c58
    bl native_fn_02004174
    mov r1, r0
    mov r0, #0
    mov r2, #32768
    bl native_fn_02008c58
    ldr r0, =0x022475ec
    mov r1, #6
    bl native_fn_02048e74
    ldr r0, =0x022475fc
    bl native_fn_02048fcc
    mov r0, #49
    bl native_fn_02063b18
    add r2, r0, #1
    ldr r0, =0x022475d4
    and r1, r2, #255
    cmp r1, #8
    strb r2, [r0]
    movhi r1, #8
    strhib r1, [r0]
    ldr r0, =0x022475d4
    mov r3, #0
    ldrb r12, [r0]
    cmp r12, #0
    ldmleia sp!, {r3, pc}
    ldr r0, =0x022475dc
ov000_0222a768_L7c:
    sub r2, r12, r3
    mov r1, r3, lsl #1
    sub r2, r2, #1
    add r3, r3, #1
    strh r2, [r0, r1]
    cmp r3, r12
    blt ov000_0222a768_L7c
    ldmia sp!, {r3, pc}
}
