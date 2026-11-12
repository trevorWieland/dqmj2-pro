/* ov000 row 0x02214120: 548 bytes.
 *
 * What it does: 124 instructions; 27 call(s) to 0x02008d78, 0x02008d78, 0x02008d78, +24 more; loops (back edge at +0x14); returns through pop {r3, pc}; 13 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1f0 -> constant 0x02245128 (image word 0x02245128)
 *   pool +0x1f4 -> constant 0x02245028 (image word 0x02245028)
 *   pool +0x1f8 -> constant 0x02244f84 (image word 0x02244f84)
 *   pool +0x1fc -> constant 0x02244efc (image word 0x02244efc)
 *   pool +0x200 -> constant 0x02244f4c (image word 0x02244f4c)
 *   pool +0x204 -> constant 0x02244f10 (image word 0x02244f10)
 *   pool +0x208 -> constant 0x02244f08 (image word 0x02244f08)
 *   pool +0x20c -> constant 0x02244fd0 (image word 0x02244fd0)
 *   pool +0x210 -> native_data_0222f890 (image word 0x0222f890)
 *   pool +0x214 -> constant 0x0000019a (image word 0x0000019a)
 *   pool +0x218 -> constant 0x022450bc (image word 0x022450bc)
 *   pool +0x21c -> constant 0x02244f1c (image word 0x02244f1c)
 *   pool +0x220 -> constant 0x00001555 (image word 0x00001555)
 *   branch +0xf0 -> +0x158
 *   test +0xec tst r0, #255
 *   0 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02214120; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_0202ac08(void);
extern void native_fn_0202a260(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_0202a44c(void);
extern void native_fn_021ea450(void);
extern u8 native_data_0222f890[];
extern void native_fn_02040d78(void);
extern void native_fn_0204106c(void);
extern void native_fn_02000ce8(void);
extern void native_fn_020280a0(void);
extern void native_fn_02028044(void);
extern void native_fn_02027fe8(void);
extern void native_fn_02000e1c(void);
extern void native_fn_0202a280(void);
extern void native_fn_02028264(void);
extern void native_fn_020282a8(void);
extern void native_fn_0202834c(void);
extern void native_fn_0202838c(void);
extern void native_fn_020283b4(void);
extern void native_fn_020283dc(void);
extern void native_fn_020283fc(void);
extern void native_fn_0202841c(void);
extern void native_fn_02028280(void);


asm u32 native_ov000_02214120 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #144
    ldr r0, =0x02245128
    mov r1, #0
    mov r2, #492
    bl native_fn_02008d78
    ldr r0, =0x02245028
    mov r1, #0
    mov r2, #256
    bl native_fn_02008d78
    ldr r0, =0x02244f84
    mov r1, #0
    mov r2, #76
    bl native_fn_02008d78
    ldr r1, =0x02244efc
    mov r2, #0
    strb r2, [r1, #0x1]
    ldr r0, =0x02244f4c
    strb r2, [r1, #0x3]
    bl native_fn_0202ac08
    bl native_fn_0202a260
    mov r0, #1
    bl native_fn_0202a1e0
    mov r0, #1
    mov r1, #52
    mov r2, #4
    bl native_fn_0202a44c
    ldr r2, =0x02244efc
    ldr r1, =0x02244f10
    str r0, [r2, #0x8]
    mov r0, #1
    ldr r2, =0x02244f08
    bl native_fn_021ea450
    ldr r0, =0x02244fd0
    ldr r1, =native_data_0222f890
    mov r2, #1
    bl native_fn_02040d78
    ldr r0, =0x02245028
    ldr r1, =0x02244fd0
    mov r2, #0
    bl native_fn_0204106c
    ldr r2, =0x0000019a
    ldr r1, =0x02245028
    ldr r0, =0x02244efc
    str r2, [r1, #0x7c]
    str r2, [r1, #0x80]
    str r2, [r1, #0x84]
    ldr r3, [r0, #0x14]
    ldr r2, [r0, #0x18]
    str r3, [r1, #0x70]
    str r2, [r1, #0x74]
    ldr r2, [r0, #0x1c]
    mov r0, #0
    str r2, [r1, #0x78]
    str r0, [r1, #0x88]
    str r0, [r1, #0x8c]
    str r0, [r1, #0x90]
    mov r0, #1
    strb r0, [r1, #0x9]
    tst r0, #255
    beq ov000_02214120_L158
    add r0, sp, #0
    bl native_fn_02000ce8
    ldr r1, =0x02245028
    add r0, sp, #36
    ldr r1, [r1, #0x90]
    bl native_fn_020280a0
    ldr r1, =0x02245028
    add r0, sp, #72
    ldr r1, [r1, #0x8c]
    bl native_fn_02028044
    ldr r1, =0x02245028
    add r0, sp, #108
    ldr r1, [r1, #0x88]
    bl native_fn_02027fe8
    add r0, sp, #72
    add r1, sp, #36
    add r2, sp, #0
    bl native_fn_02000e1c
    ldr r2, =0x022450bc
    add r0, sp, #108
    add r1, sp, #0
    bl native_fn_02000e1c
    ldr r0, =0x02245028
    mov r1, #0
    strb r1, [r0, #0x9]
ov000_02214120_L158:
    bl native_fn_0202a280
    ldr r0, =0x02244f1c
    bl native_fn_0202ac08
    ldr r0, =0x02244f84
    bl native_fn_02028264
    ldr r0, =0x02244f84
    mov r1, #122880
    bl native_fn_020282a8
    ldr r0, =0x02244f84
    ldr r1, =0x00001555
    bl native_fn_0202834c
    ldr r0, =0x02244f84
    mov r1, #4096
    bl native_fn_0202838c
    ldr r0, =0x02244f84
    mov r1, #1024000
    bl native_fn_020283b4
    ldr r0, =0x02244f84
    mov r1, #0
    mov r2, r1
    mov r3, r1
    bl native_fn_020283dc
    ldr r0, =0x02244f84
    mov r1, #0
    mov r2, r1
    mov r3, r1
    bl native_fn_020283fc
    ldr r0, =0x02244f84
    mov r1, #0
    bl native_fn_0202841c
    ldr r0, =0x02244f84
    bl native_fn_02028280
    ldr r1, =0x02244efc
    mov r2, #1
    str r0, [r1, #0x4]
    strb r2, [r1]
    add sp, sp, #144
    ldmia sp!, {r3, pc}
}
