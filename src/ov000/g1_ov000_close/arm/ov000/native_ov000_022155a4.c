/* ov000 row 0x022155a4: 92 bytes.
 *
 * What it does: 22 instructions; 7 call(s) to 0x02078968, 0x020406dc, 0x02215464, +4 more; loops (back edge at +0x08); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> constant 0x022459b4 (image word 0x022459b4)
 *   branch +0x10 -> +0x20
 *   branch +0x1c -> +0x24
 *   test +0x0c cmp r0, #1
 *   test +0x18 cmp r0, #14
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022155a4; the literal pool and
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

extern void native_fn_02078968(void);
extern void native_fn_020406dc(void);
extern void native_fn_02215464(void);
extern void native_fn_02003f80(void);
extern void native_fn_02048e74(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02214fc8(void);


asm u32 native_ov000_022155a4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
    bl native_fn_02078968
    cmp r0, #1
    beq ov000_022155a4_L20
    bl native_fn_020406dc
    cmp r0, #14
    bne ov000_022155a4_L24
ov000_022155a4_L20:
    mov r4, #1
ov000_022155a4_L24:
    mov r0, r4
    bl native_fn_02215464
    bl native_fn_02003f80
    ldr r0, =0x022459b4
    mov r1, #1
    bl native_fn_02048e74
    bl native_fn_02062aa0
    ldr r1, =0x022459b4
    strb r0, [r1, #0x495]
    mov r0, #0
    str r0, [r1, #0x4]
    bl native_fn_02214fc8
    ldmia sp!, {r4, pc}
}
