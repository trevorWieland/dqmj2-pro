/* ov001 row 0x022038b8: 496 bytes.
 *
 * What it does: 122 instructions; 29 call(s) to 0x0202a634, 0x02203418, 0x0206c120, +26 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 29 calls (122 instructions, 29 calls, 29 branches, 29 back edges, 2 literal slots).
 *
 *   pool +0x1e8 -> constant 0x00000201 (image word 0x00000201)
 *   pool +0x1ec -> constant 0x0223d8ec (image word 0x0223d8ec)
 *   branch +0x1c -> +0x68
 *   branch +0x2c -> +0x54
 *   branch +0x38 -> +0x54
 *   branch +0x48 -> +0x5c
 *   branch +0x50 -> +0x5c
 *   branch +0x74 -> +0x9c
 *   branch +0x7c -> +0x88
 *   branch +0x84 -> +0x198
 *   branch +0x8c -> +0x198
 *   branch +0x98 -> +0x198
 *   branch +0xa4 -> +0x198
 *   branch +0xb8 -> +0xe8
 *   branch +0xc8 -> +0xd4
 *   branch +0xd0 -> +0x198
 *   branch +0xd8 -> +0x198
 *   branch +0xe4 -> +0x198
 *   branch +0xec -> +0x138
 *   branch +0xf8 -> +0x11c
 *   branch +0x108 -> +0x11c
 *   branch +0x118 -> +0x198
 *   branch +0x128 -> +0x198
 *   branch +0x134 -> +0x198
 *   branch +0x13c -> +0x18c
 *   branch +0x14c -> +0x17c
 *   branch +0x178 -> +0x198
 *   branch +0x188 -> +0x198
 *   branch +0x1a8 -> +0x1dc
 *   branch +0x1b4 -> +0x1d0
 *   branch +0x1cc -> +0x1dc
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, r1
 *   test +0x34 cmp r0, #2
 *   test +0x44 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x78 cmp r0, #1
 *   test +0x88 cmp r0, #2
 *   test +0xa0 cmp r0, #0
 *   test +0xb4 tst r1, r0
 *   test +0xc4 cmp r0, #1
 *   test +0xd4 cmp r0, #2
 *   test +0xe8 tst r1, #2
 *   test +0xf4 cmp r0, #0
 *   test +0x104 cmp r0, #0
 *   test +0x124 cmp r0, #0
 *   test +0x138 tst r1, #2048
 *   test +0x148 cmp r0, #0
 *   test +0x190 cmp r0, #0
 *   test +0x1a4 cmp r5, #0
 *   test +0x1b0 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022038b8; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_02203418(void);
extern void native_fn_0206c120(void);
extern void native_fn_0206c100(void);
extern void native_fn_0206a06c(void);
extern void native_fn_02203840(void);
extern void native_fn_02203558(void);
extern void native_fn_0206a0fc(void);
extern void native_fn_0206c0b0(void);
extern void native_fn_0206940c(void);
extern void native_fn_020698f4(void);
extern void native_fn_0206c130(void);
extern void native_fn_0206be20(void);
extern void native_fn_021f949c(void);
extern void native_fn_02203610(void);
extern void native_fn_02041538(void);
extern void native_fn_0206bc80(void);
extern void native_fn_022035a0(void);
extern void native_fn_0206be08(void);


asm u32 native_ov001_022038b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #16
    bl native_fn_0202a634
    mov r4, r0
    mov r5, #0
    bl native_fn_02203418
    cmp r0, #0
    beq ov001_022038b8_L68
    bl native_fn_0206c120
    mvn r1, #0
    cmp r0, r1
    beq ov001_022038b8_L54
    bl native_fn_0206c100
    cmp r0, #2
    beq ov001_022038b8_L54
    mov r0, #1
    bl native_fn_0206a06c
    cmp r0, #0
    beq ov001_022038b8_L5c
    bl native_fn_02203840
    b ov001_022038b8_L5c
ov001_022038b8_L54:
    mov r0, #0
    bl native_fn_02203558
ov001_022038b8_L5c:
    add sp, sp, #16
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
ov001_022038b8_L68:
    mov r0, #1
    bl native_fn_0206a0fc
    cmp r0, #0
    beq ov001_022038b8_L9c
    cmp r0, #1
    bne ov001_022038b8_L88
    bl native_fn_02203840
    b ov001_022038b8_L198
ov001_022038b8_L88:
    cmp r0, #2
    bne ov001_022038b8_L198
    mov r0, r5
    bl native_fn_02203558
    b ov001_022038b8_L198
ov001_022038b8_L9c:
    bl native_fn_0206c0b0
    cmp r0, #0
    bne ov001_022038b8_L198
    bl native_fn_0206940c
    ldrh r1, [r4, #2]
    ldr r0, =0x00000201
    tst r1, r0
    beq ov001_022038b8_Le8
    mov r0, #1
    bl native_fn_020698f4
    cmp r0, #1
    bne ov001_022038b8_Ld4
    bl native_fn_02203840
    b ov001_022038b8_L198
ov001_022038b8_Ld4:
    cmp r0, #2
    bne ov001_022038b8_L198
    mov r0, r5
    bl native_fn_02203558
    b ov001_022038b8_L198
ov001_022038b8_Le8:
    tst r1, #2
    beq ov001_022038b8_L138
    bl native_fn_0206c130
    cmp r0, #0
    bne ov001_022038b8_L11c
    mov r0, #1
    bl native_fn_0206be20
    cmp r0, #0
    bne ov001_022038b8_L11c
    mov r0, #84
    mov r1, #1
    bl native_fn_021f949c
    b ov001_022038b8_L198
ov001_022038b8_L11c:
    mov r0, #1
    bl native_fn_0206a06c
    cmp r0, #0
    beq ov001_022038b8_L198
    mov r0, #0
    bl native_fn_02203558
    b ov001_022038b8_L198
ov001_022038b8_L138:
    tst r1, #2048
    beq ov001_022038b8_L18c
    bl native_fn_02203610
    ldr r0, [r0]
    cmp r0, #0
    beq ov001_022038b8_L17c
    ldr r3, =0x0223d8ec
    mov r12, #4
    mov r0, #1
    mov r1, #2
    mov r2, #10
    strb r12, [r3, #0x8]
    bl native_fn_02041538
    mov r0, #82
    mov r1, #1
    bl native_fn_021f949c
    b ov001_022038b8_L198
ov001_022038b8_L17c:
    mov r0, #84
    mov r1, #1
    bl native_fn_021f949c
    b ov001_022038b8_L198
ov001_022038b8_L18c:
    bl native_fn_0206c130
    cmp r0, #0
    moveq r5, #1
ov001_022038b8_L198:
    add r0, sp, #4
    add r1, sp, #0
    bl native_fn_0206bc80
    cmp r5, #0
    beq ov001_022038b8_L1dc
    ldrb r0, [sp]
    cmp r0, #0
    beq ov001_022038b8_L1d0
    add r0, sp, #4
    bl native_fn_022035a0
    mov r1, r0
    mov r0, #0
    bl native_fn_0206be08
    b ov001_022038b8_L1dc
ov001_022038b8_L1d0:
    mov r0, #0
    mov r1, r0
    bl native_fn_0206be08
ov001_022038b8_L1dc:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, pc}
}
