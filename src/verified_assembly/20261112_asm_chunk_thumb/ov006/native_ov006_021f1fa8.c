/* ov006 row 0x021f1fa8: 232 bytes.
 *
 * What it does: Writes 3 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd0 -> native_data9_0221aad0 (image word 0x0221aad0)
 *   pool +0xd4 -> native_data2_0220d480 (image word 0x0220d480)
 *   pool +0xd8 -> native_data2_0221ab7c (image word 0x0221ab7c)
 *   pool +0xdc -> native_fn_021f0554+1 (image word 0x021f0555)
 *   pool +0xe0 -> constant 0x0000ea60 (image word 0x0000ea60)
 *   pool +0xe4 -> constant 0x0221ac3c (image word 0x0221ac3c)
 *   branch +0x0c -> +0x1a
 *   branch +0x10 -> +0x1a
 *   branch +0x3e -> +0x46
 *   branch +0x54 -> +0x60
 *   branch +0x66 -> +0x74
 *   back edge +0xb8 -> +0xb2
 *   test +0x0a cmp r0, #0x1
 *   test +0x0e cmp r0, #0x5
 *   test +0x3a cmp r0, #0x0
 *   test +0x50 cmp r0, #0x0
 *   test +0x64 cmp r0, #0x1
 *   3 block transfer(s), 17 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f1fa8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 232 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data9_0221aad0[];
extern u8 native_data2_0220d480[];
extern void native_fn_021ef114(void);
extern void native_fn_020065e0(void);
extern u8 native_data2_0221ab7c[];
extern void native_fn_021f0554(void);
extern void native_fn_020065f0(void);
extern void native_fn_021f1ef0(void);
extern void native_fn_021f2170(void);
extern void native_fn_0200698c(void);


asm u32 native_ov006_021f1fa8 (register u32 a0)
{
    push {r4, r5, r6, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =native_data9_0221aad0
    ldr r0, [r0, #0x38]
    cmp r0, #0x1
    blt ov006_021f1fa8_L1a
    cmp r0, #0x5
    bgt ov006_021f1fa8_L1a
    mov r0, #0x9
    add sp, #0x8
    mvn r0, r0
    pop {r4, r5, r6, pc}
ov006_021f1fa8_L1a:
    ldr r5, =native_data2_0220d480
    ldr r0, =native_data9_0221aad0
    mov r6, #0x7
    str r1, [r5, #0x10]
    str r6, [r0, #0x38]
    str r2, [r0, #0x7c]
    ldr r2, [sp, #0x18]
    str r3, [r0, #0x4]
    str r2, [r0, #0xc]
    ldr r0, [sp, #0x1c]
    str r0, [r5, #0x8]
    add r0, r1, #0x0
    bl native_fn_021ef114
    mov r2, #0x1
    ldr r1, =native_data9_0221aad0
    cmp r0, #0x0
    str r2, [r1, #0x74]
    bge ov006_021f1fa8_L46
    str r0, [r1, #0x78]
    add sp, #0x8
    pop {r4, r5, r6, pc}
ov006_021f1fa8_L46:
    add r0, r5, #0x0
    ldr r0, [r0, #0x8]
    ldr r1, [r1, #0x4]
    blx r1
    ldr r1, =native_data9_0221aad0
    cmp r0, #0x0
    str r0, [r1, #0x30]
    bne ov006_021f1fa8_L60
    add r0, r6, #0x0
    sub r0, #0x8
    str r0, [r1, #0x78]
    add sp, #0x8
    pop {r4, r5, r6, pc}
ov006_021f1fa8_L60:
    blx native_fn_020065e0
    cmp r0, #0x1
    beq ov006_021f1fa8_L74
    add r0, r6, #0x0
    ldr r1, =native_data9_0221aad0
    sub r0, #0x10
    str r0, [r1, #0x78]
    add sp, #0x8
    pop {r4, r5, r6, pc}
ov006_021f1fa8_L74:
    add r0, r5, #0x0
    ldr r3, [r0, #0x8]
    ldr r0, =native_data2_0221ab7c
    str r3, [sp]
    str r4, [sp, #0x4]
    ldr r4, =native_data9_0221aad0
    ldr r1, =native_fn_021f0554+1
    ldr r5, [r4, #0x30]
    mov r4, #0x7
    bic r3, r4
    mov r2, #0x0
    add r3, r5, r3
    blx native_fn_020065f0
    ldr r0, =native_data9_0221aad0
    mov r1, #0x1
    str r1, [r0, #0x38]
    bl native_fn_021f1ef0
    ldr r1, =0x0000ea60
    ldr r5, =0x0221ac3c
    add r1, r0, r1
    ldr r0, =native_data2_0220d480
    add r4, r6, #0x0
    str r1, [r0, #0xc]
    mov r0, #0x0
    ldr r1, =native_data9_0221aad0
    add r2, r0, #0x0
    str r0, [r1, #0x10]
    add r1, r0, #0x0
    add r3, r0, #0x0
ov006_021f1fa8_Lb2:
    stmia r5!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    sub r4, r4, #0x1
    bne ov006_021f1fa8_Lb2
    stmia r5!, {r0, r1}
    bl native_fn_021f2170
    ldr r0, =native_data2_0221ab7c
    blx native_fn_0200698c
    ldr r1, =native_data9_0221aad0
    mov r0, #0x1
    str r0, [r1, #0x64]
    add sp, #0x8
    pop {r4, r5, r6, pc}
}
