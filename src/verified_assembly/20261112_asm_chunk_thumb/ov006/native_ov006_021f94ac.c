/* ov006 row 0x021f94ac: 248 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (2 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xe0 -> native_data_0220b6a0 (image word 0x0220b6a0)
 *   pool +0xe4 -> native_data_0220b688 (image word 0x0220b688)
 *   pool +0xe8 -> native_data6_0221c0e4 (image word 0x0221c0e4)
 *   pool +0xec -> native_data_0220dde8 (image word 0x0220dde8)
 *   pool +0xf0 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0xf4 -> native_fn_021f9624+1 (image word 0x021f9625)
 *   branch +0x62 -> +0x6a
 *   branch +0x68 -> +0x7e
 *   test +0x60 cmp r0, #0x0
 *   4 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f94ac; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 11 of 248 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b6a0[];
extern u8 native_data_0220b688[];
extern void native_fn_02203c08(void);
extern u8 native_data6_0221c0e4[];
extern void native_fn_021f530c(void);
extern u8 native_data_0220dde8[];
extern void native_fn_0201b248(void);
extern void native_fn_02008d78(void);
extern void native_fn_021f95a4(void);
extern void native_fn_021f2ad4(void);
extern void native_fn_021f26f0(void);
extern void native_fn_021f27fc(void);
extern void native_fn_022034dc(void);
extern void native_fn_0220303c(void);
extern void native_fn_021f9ac4(void);
extern void native_fn_021f9a44(void);
extern void native_fn_021f9624(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f94ac (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x20
    ldr r3, =native_data_0220b6a0
    add r2, sp, #0xc
    ldmia r3!, {r0, r1}
    stmia r2!, {r0, r1}
    ldmia r3!, {r0, r1}
    stmia r2!, {r0, r1}
    ldr r0, [r3, #0]
    ldr r1, =native_data_0220b688
    str r0, [r2, #0]
    ldrb r2, [r1, #0x8]
    add r0, sp, #0x0
    strb r2, [r0, #0x4]
    ldrb r2, [r1, #0x9]
    strb r2, [r0, #0x5]
    ldrb r2, [r1, #0xa]
    strb r2, [r0, #0x6]
    ldrb r2, [r1, #0xb]
    ldrb r1, [r1, #0xc]
    strb r2, [r0, #0x7]
    strb r1, [r0, #0x8]
    mov r0, #0x18
    mov r1, #0x4
    bl native_fn_02203c08
    ldr r1, =native_data6_0221c0e4
    str r0, [r1, #0]
    add r0, sp, #0x0
    mov r1, #0x0
    bl native_fn_021f530c
    ldr r0, =native_data6_0221c0e4
    ldr r1, [sp]
    ldr r0, [r0, #0]
    lsl r2, r1, #0x2
    add r1, sp, #0xc
    ldr r1, [r1, r2]
    add r0, #0x8
    blx r1
    ldr r0, =native_data6_0221c0e4
    ldr r1, =native_data_0220dde8
    ldr r4, [r0, #0]
    mov r2, #0x3
    add r0, r4, #0x0
    add r0, #0x8
    blx native_fn_0201b248
    cmp r0, #0x0
    beq ov006_021f94ac_L6a
    mov r0, #0x3
    strb r0, [r4, #0x14]
    b ov006_021f94ac_L7e
ov006_021f94ac_L6a:
    add r4, #0x8
    add r0, r4, #0x0
    mov r1, #0x0
    mov r2, #0xc
    blx native_fn_02008d78
    ldr r0, =native_data6_0221c0e4
    mov r1, #0x0
    ldr r0, [r0, #0]
    strb r1, [r0, #0x14]
ov006_021f94ac_L7e:
    bl native_fn_021f95a4
    ldr r0, [sp]
    add r0, #0xb
    bl native_fn_021f2ad4
    ldr r1, [sp]
    add r0, sp, #0x4
    ldrb r0, [r0, r1]
    mov r1, #0x0
    mvn r1, r1
    mov r2, #0x0
    bl native_fn_021f26f0
    mov r0, #0x2
    bl native_fn_021f27fc
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_022034dc
    ldr r1, =native_data6_0221c0e4
    ldr r1, [r1, #0]
    str r0, [r1, #0]
    mov r0, #0x0
    mov r1, #0x3f
    bl native_fn_0220303c
    ldr r1, =native_data6_0221c0e4
    ldr r2, [r1, #0]
    str r0, [r2, #0x4]
    ldr r0, [r1, #0]
    ldr r2, [r0, #0x4]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x3
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
    bl native_fn_021f9ac4
    bl native_fn_021f9a44
    ldr r0, =native_fn_021f9624+1
    bl native_fn_021f52cc
    add sp, #0x20
    pop {r4, pc}
}
