/* ov001 row 0x02212878: 132 bytes.
 *
 * What it does: 33 instructions; 5 call(s) to 0x0205f98c, 0x02048a60, 0x02048a94, +2 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 5 calls (33 instructions, 5 calls, 0 branches, 5 back edges, 0 literal slots).
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02212878; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern void native_fn_021f1ba0(void);


asm u32 native_ov001_02212878 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldr r0, [r5, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldrsh r1, [r5, #20]
    ldrsh r2, [r5, #22]
    mov r4, r0
    bl native_fn_02048a60
    ldr r1, [r4, #0x7c]
    mov r0, r4
    orr r1, r1, #2
    str r1, [r4, #0x7c]
    ldrb r1, [r5, #0x20]
    bl native_fn_02048a94
    ldrb r1, [r5, #0x21]
    mov r0, r4
    bl native_fn_02048a9c
    ldr r1, [r4, #0x7c]
    mov r0, r4
    orr r1, r1, #2
    str r1, [r4, #0x7c]
    ldr r1, [r5, #0x2c]
    and r1, r1, #255
    bl native_fn_021f1ba0
    mov r1, #60
    strh r1, [r5, #38]
    mov r1, #1
    mov r0, #6
    strb r1, [r5, #0x24]
    strh r0, [r4, #142]
    strh r0, [r5, #26]
    ldmia sp!, {r3, r4, r5, pc}
}
