/* ov006 row 0x021d7f68: 384 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x164 -> constant 0xffcfffef (image word 0xffcfffef)
 *   pool +0x168 -> native_data_0220c8a0 (image word 0x0220c8a0)
 *   pool +0x16c -> native_data2_0220e9a0 (image word 0x0220e9a0)
 *   pool +0x170 -> constant 0x0220ea74 (image word 0x0220ea74)
 *   pool +0x174 -> constant 0x0220eba4 (image word 0x0220eba4)
 *   pool +0x178 -> constant 0x0220ed54 (image word 0x0220ed54)
 *   pool +0x17c -> constant 0x55555556 (image word 0x55555556)
 *   back edge +0xe8 -> +0xc0
 *   back edge +0x150 -> +0x110
 *   test +0xdc cmp r7, #3
 *   test +0x144 cmp r10, #10
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021d7f68; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020489f0(void);
extern void native_fn_02008c58(void);
extern void native_fn_02048404(void);
extern u8 native_data_0220c8a0[];
extern void native_fn_0204854c(void);
extern u8 native_data2_0220e9a0[];
extern void native_fn_02048308(void);
extern void native_fn_021d81b0(void);
extern void native_fn_021d8288(void);
extern void native_fn_021d8328(void);


asm u32 native_ov006_021d7f68 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #4
    mov r5, r0
    mov r0, #0
    mov r4, r1
    bl native_fn_020489f0
    mov r0, #1
    bl native_fn_020489f0
    mov r3, #67108864
    ldr r2, [r3]
    ldr r1, =0xffcfffef
    mov r0, #0
    and r1, r2, r1
    orr r1, r1, #16
    str r1, [r3]
    mov r1, #104857600
    mov r2, #262144
    bl native_fn_02008c58
    mov r1, r5
    mov r2, r4
    mov r0, #0
    mov r3, #2
    bl native_fn_02048404
    mov r2, r0
    ldr r1, =native_data_0220c8a0
    mov r0, #0
    strb r2, [r1]
    and r1, r2, #255
    bl native_fn_0204854c
    ldr r1, =native_data2_0220e9a0
    str r0, [r1, #0x10]
    ldr r0, [r0, #0x4]
    str r0, [r1, #0x1c]
    bl native_fn_02048308
    ldr r1, =native_data2_0220e9a0
    mov r2, #0
    strb r2, [r1]
    ldr r0, =0x0220ea74
    mov r1, #240
    mov r3, #3
    str r2, [sp]
    bl native_fn_021d81b0
    mov r7, #0
    ldr r9, =0x0220eba4
    mov r8, #64
    mov r6, #4
    mov r5, #24
    mov r4, r7
ov006_021d7f68_Lc0:
    mov r0, r9
    mov r1, r5
    mov r2, r8
    mov r3, r4
    str r6, [sp]
    bl native_fn_021d81b0
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #40
    add r9, r9, #144
    blt ov006_021d7f68_Lc0
    mov r0, #0
    bl native_fn_021d8288
    mov r10, #0
    ldr r9, =0x0220ed54
    ldr r5, =0x55555556
    mov r8, #24
    mov r7, #8
    mov r6, r10
    mov r4, #3
ov006_021d7f68_L110:
    smull r0, r1, r5, r10
    add r1, r1, r10, lsr #31
    smull r0, r1, r4, r1
    sub r1, r10, r0
    add r0, r1, #8
    and r12, r0, #255
    mov r0, r9
    mov r1, r7
    mov r2, r8
    mov r3, r6
    str r12, [sp]
    bl native_fn_021d81b0
    add r10, r10, #1
    cmp r10, #10
    add r8, r8, #16
    add r9, r9, #144
    blt ov006_021d7f68_L110
    mov r0, #0
    bl native_fn_021d8328
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
