/* ov000 row 0x021e9e74: 1000 bytes.
 *
 * What it does: 240 instructions; 49 call(s) to 0x0202a090, 0x02040808, 0x0202a44c, +46 more; loops (back edge at +0x10); returns through pop {r3, pc}; 10 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x3c0 -> constant 0x02236950 (image word 0x02236950)
 *   pool +0x3c4 -> native_data_0222edd4 (image word 0x0222edd4)
 *   pool +0x3c8 -> constant 0x00001555 (image word 0x00001555)
 *   pool +0x3cc -> constant 0x00000a58 (image word 0x00000a58)
 *   pool +0x3d0 -> constant 0x00000ba8 (image word 0x00000ba8)
 *   pool +0x3d4 -> constant 0xfffff6d8 (image word 0xfffff6d8)
 *   pool +0x3d8 -> constant 0x000001b2 (image word 0x000001b2)
 *   pool +0x3dc -> constant 0x0000013b (image word 0x0000013b)
 *   pool +0x3e0 -> native_data_0222edc4 (image word 0x0222edc4)
 *   pool +0x3e4 -> constant 0x0000019a (image word 0x0000019a)
 *   branch +0x274 -> +0x390
 *   branch +0x310 -> +0x390
 *   test +0x270 cmp r0, #0
 *   test +0x30c cmp r0, #0
 *   0 block transfer(s), 24 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e9e74; the literal pool and
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

extern void native_fn_0202a090(void);
extern void native_fn_02040808(void);
extern void native_fn_0202a44c(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_0207a9ec(void);
extern void native_fn_02029c88(void);
extern void native_fn_02040820(void);
extern void native_fn_021ea450(void);
extern u8 native_data_0222edd4[];
extern void native_fn_02042fec(void);
extern void native_fn_02028264(void);
extern void native_fn_02028280(void);
extern void native_fn_020282a8(void);
extern void native_fn_0202834c(void);
extern void native_fn_0202838c(void);
extern void native_fn_020283b4(void);
extern void native_fn_020283dc(void);
extern void native_fn_020283fc(void);
extern void native_fn_0202841c(void);
extern void native_fn_021dfe0c(void);
extern void native_fn_0205c3c4(void);
extern void native_fn_021dfe5c(void);
extern void native_fn_021dfe80(void);
extern void native_fn_021dfea4(void);
extern void native_fn_02029d84(void);
extern void native_fn_021eaa50(void);
extern u8 native_data_0222edc4[];
extern void native_fn_02040d78(void);
extern void native_fn_0204106c(void);
extern void native_fn_02000ce8(void);
extern void native_fn_020280a0(void);
extern void native_fn_02028044(void);
extern void native_fn_02027fe8(void);
extern void native_fn_02000e1c(void);
extern void native_fn_0202ac08(void);


asm u32 native_ov000_021e9e74 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #144
    mov r0, #1
    mov r1, #1081344
    bl native_fn_0202a090
    bl native_fn_02040808
    mov r0, #1
    mov r1, #504
    mov r2, #4
    bl native_fn_0202a44c
    ldr r1, =0x02236950
    mov r2, #0
    str r0, [r1, #0x18]
    strb r2, [r1, #0x6]
    strb r2, [r1, #0x2]
    strb r2, [r1]
    strb r2, [r1, #0x5]
    strb r2, [r1, #0x4]
    mov r0, #2
    bl native_fn_0202a1e0
    mov r0, #2
    bl native_fn_0207a9ec
    mov r0, #0
    mov r1, r0
    mov r2, r0
    bl native_fn_02029c88
    bl native_fn_02040820
    ldr r1, =0x02236950
    mov r0, #1
    ldr r2, [r1, #0x18]
    add r1, r2, #480
    add r2, r2, #492
    bl native_fn_021ea450
    ldr r0, =native_data_0222edd4
    mov r1, #2
    bl native_fn_02042fec
    mov r0, #1
    mov r1, #76
    mov r2, #4
    bl native_fn_0202a44c
    ldr r1, =0x02236950
    str r0, [r1, #0x8]
    bl native_fn_02028264
    ldr r0, =0x02236950
    ldr r0, [r0, #0x8]
    bl native_fn_02028280
    mov r0, #0
    mov r1, #122880
    bl native_fn_020282a8
    mov r0, #0
    ldr r1, =0x00001555
    bl native_fn_0202834c
    mov r0, #0
    mov r1, #4096
    bl native_fn_0202838c
    mov r0, #0
    mov r1, #4096000
    bl native_fn_020283b4
    mov r0, #0
    mov r1, r0
    mov r2, r0
    mov r3, r0
    bl native_fn_020283dc
    mov r0, #0
    mov r1, r0
    mov r2, r0
    mov r3, r0
    bl native_fn_020283fc
    mov r0, #0
    mov r1, r0
    bl native_fn_0202841c
    mov r0, #1
    mov r1, #52
    mov r2, #4
    bl native_fn_0202a44c
    ldr r1, =0x02236950
    mov r2, #0
    str r0, [r1, #0x20]
    strb r2, [r1, #0x7]
    bl native_fn_021dfe0c
    bl native_fn_0205c3c4
    mov r0, #0
    ldr r1, =0x00000a58
    rsb r2, r1, #56
    rsb r3, r1, #920
    bl native_fn_021dfe5c
    mov r0, #0
    mov r1, #23
    mov r2, r1
    mov r3, r1
    bl native_fn_021dfe80
    mov r0, #0
    mov r1, #1
    bl native_fn_021dfea4
    mov r0, #1
    ldr r1, =0x00000ba8
    mov r2, #808
    sub r3, r2, #3488
    bl native_fn_021dfe5c
    mov r0, #1
    mov r1, #14
    mov r2, r1
    mov r3, r1
    bl native_fn_021dfe80
    mov r0, #1
    mov r1, r0
    bl native_fn_021dfea4
    mov r0, #2
    ldr r1, =0xfffff6d8
    sub r2, r1, #400
    add r3, r1, #424
    bl native_fn_021dfe5c
    mov r0, #2
    mov r1, #8
    mov r2, r1
    mov r3, r1
    bl native_fn_021dfe80
    mov r0, #2
    mov r1, #1
    bl native_fn_021dfea4
    mov r1, #1728
    rsb r1, r1, #0
    mov r0, #3
    mov r2, #600
    mov r3, #3664
    bl native_fn_021dfe5c
    mov r1, #4
    mov r2, r1
    mov r3, r1
    mov r0, #3
    bl native_fn_021dfe80
    mov r0, #3
    mov r1, #1
    bl native_fn_021dfea4
    mov r0, #0
    bl native_fn_02029d84
    ldr r0, =0x000001b2
    bl native_fn_021eaa50
    ldr r0, =0x0000013b
    bl native_fn_021eaa50
    mov r0, #1
    mov r1, #88
    mov r2, #4
    bl native_fn_0202a44c
    ldr r2, =0x02236950
    mov r1, #256
    str r0, [r2, #0x10]
    mov r0, #1
    mov r2, #4
    bl native_fn_0202a44c
    ldr r2, =0x02236950
    ldr r1, =native_data_0222edc4
    str r0, [r2, #0xc]
    ldr r0, [r2, #0x10]
    mov r2, #1
    bl native_fn_02040d78
    cmp r0, #0
    beq ov000_021e9e74_L390
    ldr r1, =0x02236950
    mov r2, #0
    ldr r0, [r1, #0xc]
    ldr r1, [r1, #0x10]
    bl native_fn_0204106c
    ldr r0, =0x02236950
    ldr r12, =0x0000019a
    ldr r1, [r0, #0xc]
    mov r3, #0
    str r12, [r1, #0x7c]
    ldr r1, [r0, #0xc]
    mov r2, #1
    str r12, [r1, #0x80]
    ldr r1, [r0, #0xc]
    str r12, [r1, #0x84]
    ldr r12, [r0, #0x18]
    ldr r1, [r0, #0xc]
    ldr r12, [r12, #0x1e0]
    str r12, [r1, #0x70]
    ldr r12, [r0, #0x18]
    ldr r1, [r0, #0xc]
    ldr r12, [r12, #0x1e4]
    str r12, [r1, #0x74]
    ldr r12, [r0, #0x18]
    ldr r1, [r0, #0xc]
    ldr r12, [r12, #0x1e8]
    str r12, [r1, #0x78]
    ldr r1, [r0, #0xc]
    str r3, [r1, #0x88]
    ldr r1, [r0, #0xc]
    str r3, [r1, #0x8c]
    ldr r1, [r0, #0xc]
    str r3, [r1, #0x90]
    ldr r1, [r0, #0xc]
    strb r2, [r1, #0x9]
    ldr r0, [r0, #0xc]
    ldrb r0, [r0, #0x9]
    cmp r0, #0
    beq ov000_021e9e74_L390
    add r0, sp, #0
    bl native_fn_02000ce8
    ldr r1, =0x02236950
    add r0, sp, #36
    ldr r1, [r1, #0xc]
    ldr r1, [r1, #0x90]
    bl native_fn_020280a0
    ldr r1, =0x02236950
    add r0, sp, #72
    ldr r1, [r1, #0xc]
    ldr r1, [r1, #0x8c]
    bl native_fn_02028044
    ldr r1, =0x02236950
    add r0, sp, #108
    ldr r1, [r1, #0xc]
    ldr r1, [r1, #0x88]
    bl native_fn_02027fe8
    add r0, sp, #72
    add r1, sp, #36
    add r2, sp, #0
    bl native_fn_02000e1c
    ldr r2, =0x02236950
    add r0, sp, #108
    ldr r2, [r2, #0xc]
    add r1, sp, #0
    add r2, r2, #148
    bl native_fn_02000e1c
    ldr r0, =0x02236950
    mov r1, #0
    ldr r0, [r0, #0xc]
    strb r1, [r0, #0x9]
ov000_021e9e74_L390:
    mov r0, #1
    mov r1, #48
    mov r2, #4
    bl native_fn_0202a44c
    ldr r1, =0x02236950
    str r0, [r1, #0x14]
    bl native_fn_0202ac08
    ldr r0, =0x02236950
    mvn r1, #0
    str r1, [r0, #0x28]
    add sp, sp, #144
    ldmia sp!, {r3, pc}
}
