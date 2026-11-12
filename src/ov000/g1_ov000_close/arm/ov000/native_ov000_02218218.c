/* ov000 row 0x02218218: 92 bytes.
 *
 * What it does: 20 instructions; 6 call(s) to 0x022184fc, 0x02218274, 0x02048308, +3 more; loops (back edge at +0x0c); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x50 -> constant 0x02245e94 (image word 0x02245e94)
 *   pool +0x54 -> constant 0x02245ea0 (image word 0x02245ea0)
 *   pool +0x58 -> constant 0x02245e54 (image word 0x02245e54)
 *   2 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218218; the literal pool and
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

extern void native_fn_022184fc(void);
extern void native_fn_02218274(void);
extern void native_fn_02048308(void);
extern void native_fn_022199b8(void);
extern void native_fn_02219ce4(void);
extern void native_fn_02219c88(void);


asm u32 native_ov000_02218218 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_022184fc
    bl native_fn_02218274
    bl native_fn_02048308
    bl native_fn_022199b8
    ldr r0, =0x02245e94
    bl native_fn_02219ce4
    bl native_fn_02219c88
    ldr r0, =0x02245ea0
    ldr lr, =0x02245e94
    ldmia r0, {r0, r1, r2}
    stmia lr, {r0, r1, r2}
    ldr r3, =0x02245e54
    mov r12, #0
    strh r12, [r3, #18]
    strh r12, [r3, #16]
    str r12, [r3, #0x20]
    str r12, [r3, #0x28]
    strb r12, [r3, #0x3]
    ldmia sp!, {r3, pc}
}
