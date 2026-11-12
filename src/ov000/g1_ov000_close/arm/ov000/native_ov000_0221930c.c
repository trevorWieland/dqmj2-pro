/* ov000 row 0x0221930c: 128 bytes.
 *
 * What it does: 29 instructions; 9 call(s) to 0x02218534, 0x0205f998, 0x02219324, +6 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x74 -> constant 0x02245ee4 (image word 0x02245ee4)
 *   pool +0x78 -> native_data_0222fa08 (image word 0x0222fa08)
 *   pool +0x7c -> constant 0x02245e54 (image word 0x02245e54)
 *   back edge +0x2c -> +0x18
 *   test +0x28 cmp r6, #2
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221930c; the literal pool and
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

extern void native_fn_02218534(void);
extern void native_fn_0205f998(void);
extern void native_fn_02218628(void);
extern void native_fn_021df1f0(void);
extern u8 native_data_0222fa08[];
extern void native_fn_02218330(void);
extern void native_fn_022188cc(void);
extern void native_fn_02218990(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_0221930c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r0, #0
    bl native_fn_02218534
    ldr r5, =0x02245ee4
    mov r6, #0
    mov r4, #72
ov000_0221930c_L18:
    mla r0, r6, r4, r5
    bl native_fn_0205f998
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, #2
    blo ov000_0221930c_L18
    bl native_fn_02218628
    bl native_fn_021df1f0
    ldr r1, =native_data_0222fa08
    strb r0, [r1, #0x1]
    and r0, r0, #255
    bl native_fn_02218330
    ldr r0, =native_data_0222fa08
    mov r1, #255
    strb r1, [r0, #0x4]
    ldrb r0, [r0, #0x1]
    bl native_fn_022188cc
    bl native_fn_02218990
    bl native_fn_02048308
    ldr r0, =0x02245e54
    mov r1, #1
    str r1, [r0, #0x30]
    ldmia sp!, {r4, r5, r6, pc}
}
