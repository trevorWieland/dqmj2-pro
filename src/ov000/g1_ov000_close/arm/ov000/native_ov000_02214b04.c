/* ov000 row 0x02214b04: 512 bytes.
 *
 * What it does: 115 instructions; 38 call(s) to 0x021e07b8, 0x02041f74, 0x0200285c, +35 more; loops (back edge at +0x10); returns through pop {r4, pc}; 13 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1cc -> constant 0x45800000 (image word 0x45800000)
 *   pool +0x1d0 -> constant 0x42c80000 (image word 0x42c80000)
 *   pool +0x1d4 -> constant 0x42b40000 (image word 0x42b40000)
 *   pool +0x1d8 -> constant 0x42a00000 (image word 0x42a00000)
 *   pool +0x1dc -> constant 0x428c0000 (image word 0x428c0000)
 *   pool +0x1e0 -> constant 0x42700000 (image word 0x42700000)
 *   pool +0x1e4 -> constant 0x42480000 (image word 0x42480000)
 *   pool +0x1e8 -> constant 0x42200000 (image word 0x42200000)
 *   pool +0x1ec -> constant 0x41f00000 (image word 0x41f00000)
 *   pool +0x1f0 -> constant 0x41a00000 (image word 0x41a00000)
 *   pool +0x1f4 -> constant 0x41200000 (image word 0x41200000)
 *   pool +0x1f8 -> constant 0x00000171 (image word 0x00000171)
 *   pool +0x1fc -> constant 0x0000019a (image word 0x0000019a)
 *   branch +0x44 -> +0x5c
 *   branch +0x58 -> +0x1c0
 *   branch +0x68 -> +0x80
 *   branch +0x7c -> +0x1c0
 *   branch +0x8c -> +0xa4
 *   branch +0xa0 -> +0x1c0
 *   branch +0xb0 -> +0xc8
 *   branch +0xc4 -> +0x1c0
 *   branch +0xd4 -> +0xec
 *   branch +0xe8 -> +0x1c0
 *   branch +0xf8 -> +0x110
 *   branch +0x10c -> +0x1c0
 *   branch +0x11c -> +0x134
 *   branch +0x130 -> +0x1c0
 *   branch +0x140 -> +0x158
 *   branch +0x154 -> +0x1c0
 *   branch +0x164 -> +0x17c
 *   branch +0x178 -> +0x1c0
 *   branch +0x188 -> +0x1a0
 *   branch +0x19c -> +0x1c0
 *   branch +0x1ac -> +0x1c0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02214b04; the literal pool and
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

extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_02041f74(void);
extern void native_fn_0200285c(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_0202537c(void);
extern void native_fn_021d8ccc(void);


asm u32 native_ov000_02214b04 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #24
    mov r4, r0
    add r0, sp, #0
    bl ov000_saved_world_position_get_021e07b8
    add r1, sp, #12
    mov r0, r4
    bl native_fn_02041f74
    add r0, sp, #0
    add r1, sp, #12
    bl native_fn_0200285c
    bl native_fn_02025a28
    ldr r1, =0x45800000
    bl native_fn_02025578
    ldr r1, =0x42c80000
    mov r4, r0
    bl native_fn_0202537c
    bls ov000_02214b04_L5c
    mov r0, #800
    mov r1, #100
    mov r2, #0
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L5c:
    ldr r1, =0x42b40000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_L80
    mov r0, #800
    mov r1, #100
    mov r2, #41
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L80:
    ldr r1, =0x42a00000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_La4
    mov r0, #800
    mov r1, #100
    mov r2, #82
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_La4:
    ldr r1, =0x428c0000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_Lc8
    mov r0, #800
    mov r1, #100
    mov r2, #123
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_Lc8:
    ldr r1, =0x42700000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_Lec
    mov r0, #800
    mov r1, #100
    mov r2, #164
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_Lec:
    ldr r1, =0x42480000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_L110
    mov r0, #800
    mov r1, #100
    mov r2, #205
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L110:
    ldr r1, =0x42200000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_L134
    mov r0, #800
    mov r1, #100
    mov r2, #246
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L134:
    ldr r1, =0x41f00000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_L158
    mov r1, #100
    add r2, r1, #187
    mov r0, #1600
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L158:
    ldr r1, =0x41a00000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_L17c
    mov r0, #3200
    mov r1, #100
    mov r2, #328
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L17c:
    ldr r1, =0x41200000
    mov r0, r4
    bl native_fn_0202537c
    bls ov000_02214b04_L1a0
    ldr r2, =0x00000171
    mov r0, #6400
    mov r1, #100
    bl native_fn_021d8ccc
    b ov000_02214b04_L1c0
ov000_02214b04_L1a0:
    mov r0, r4
    mov r1, #0
    bl native_fn_0202537c
    bls ov000_02214b04_L1c0
    ldr r2, =0x0000019a
    mov r0, #12800
    mov r1, #100
    bl native_fn_021d8ccc
ov000_02214b04_L1c0:
    mov r0, #0
    add sp, sp, #24
    ldmia sp!, {r4, pc}
}
