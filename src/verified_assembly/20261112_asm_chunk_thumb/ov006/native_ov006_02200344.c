/* ov006 row 0x02200344: 516 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1d0 -> native_data_0220ba80 (image word 0x0220ba80)
 *   pool +0x1d4 -> constant 0x0221c098 (image word 0x0221c098)
 *   pool +0x1d8 -> native_data13_0221c15c (image word 0x0221c15c)
 *   pool +0x1dc -> constant 0x04000050 (image word 0x04000050)
 *   pool +0x1e0 -> native_data_0220bb34 (image word 0x0220bb34)
 *   pool +0x1e4 -> native_data2_0220bb3c (image word 0x0220bb3c)
 *   pool +0x1e8 -> native_data_0220baa6 (image word 0x0220baa6)
 *   pool +0x1ec -> native_data_0220bac6 (image word 0x0220bac6)
 *   pool +0x1f0 -> native_data_0220bac4 (image word 0x0220bac4)
 *   pool +0x1f4 -> native_data_0220ba8a (image word 0x0220ba8a)
 *   pool +0x1f8 -> constant 0xffff1fff (image word 0xffff1fff)
 *   pool +0x1fc -> native_fn_02200598+1 (image word 0x02200599)
 *   pool +0x200 -> native_fn_022005d8+1 (image word 0x022005d9)
 *   branch +0x98 -> +0xea
 *   back edge +0xe8 -> +0xa2
 *   branch +0x1a0 -> +0x1b8
 *   test +0x96 cmp r0, #0x0
 *   test +0xe6 cmp r4, r0
 *   test +0x19e cmp r0, #0x0
 *   0 block transfer(s), 26 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200344; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 516 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220ba80[];
extern void native_fn_021f5428(void);
extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data13_0221c15c[];
extern void native_fn_020042e0(void);
extern u8 native_data_0220bb34[];
extern void native_fn_02203058(void);
extern void native_fn_02202eb0(void);
extern void native_fn_02202f54(void);
extern u8 native_data2_0220bb3c[];
extern u8 native_data_0220baa6[];
extern void native_fn_0220342c(void);
extern void native_fn_02202c5c(void);
extern void native_fn_021f290c(void);
extern u8 native_data_0220bac6[];
extern u8 native_data_0220bac4[];
extern void native_fn_022037c0(void);
extern void native_fn_02203848(void);
extern void native_fn_02203a80(void);
extern u8 native_data_0220ba8a[];
extern void native_fn_022039a4(void);
extern void native_fn_02200770(void);
extern void native_fn_02200598(void);
extern void native_fn_0220490c(void);
extern void native_fn_022005d8(void);


asm u32 native_ov006_02200344 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x24
    add r7, r1, #0x0
    ldr r1, =native_data_0220ba80
    str r2, [sp, #0x10]
    ldrb r2, [r1, #0x4]
    add r4, r0, #0x0
    add r0, sp, #0x18
    strb r2, [r0, #0x4]
    ldrb r2, [r1, #0x5]
    strb r2, [r0, #0x5]
    ldrb r2, [r1, #0x6]
    strb r2, [r0, #0x6]
    ldrb r2, [r1, #0x7]
    strb r2, [r0, #0x7]
    ldrb r2, [r1, #0x8]
    ldrb r1, [r1, #0x9]
    strb r2, [r0, #0x8]
    strb r1, [r0, #0x9]
    ldr r0, =0x0221c098
    add r2, r3, #0x0
    ldr r0, [r0, #0]
    ldr r3, [sp, #0x38]
    add r1, r4, #0x0
    bl native_fn_021f5428
    str r0, [sp, #0x14]
    mov r0, #0x20
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r1, =native_data13_0221c15c
    mov r2, #0x1
    str r0, [r1, #0]
    strb r7, [r0, #0x1c]
    ldr r0, [r1, #0]
    mvn r2, r2
    strb r2, [r0, #0x1b]
    ldr r1, [r1, #0]
    ldr r0, [sp, #0x10]
    mov r2, #0x0
    strb r0, [r1, #0x1e]
    ldr r0, =0x04000050
    mov r1, #0x1f
    blx native_fn_020042e0
    ldr r1, =native_data_0220bb34
    mov r0, #0x0
    ldrb r1, [r1, r7]
    add r2, r0, #0x0
    bl native_fn_02203058
    ldr r1, =native_data13_0221c15c
    mov r3, #0x0
    ldr r2, [r1, #0]
    str r0, [r2, #0]
    ldr r0, [r1, #0]
    mov r1, #0x0
    mov r2, #0x1
    ldr r0, [r0, #0]
    mvn r1, r1
    lsl r2, r2, #0x8
    bl native_fn_02202eb0
    ldr r0, =native_data13_0221c15c
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, #0]
    mov r2, #0x0
    bl native_fn_02202f54
    ldr r0, =native_data2_0220bb3c
    mov r4, #0x0
    ldrb r0, [r0, r7]
    cmp r0, #0x0
    ble ov006_02200344_Lea
    ldr r1, =native_data_0220baa6
    lsl r0, r7, #0x1
    add r6, r1, r0
    add r5, r4, #0x0
ov006_02200344_La2:
    ldrb r1, [r6, #0]
    mov r0, #0x0
    add r2, r0, #0x0
    bl native_fn_02203058
    ldr r1, =native_data13_0221c15c
    mov r2, #0x1
    ldr r1, [r1, #0]
    lsl r2, r2, #0x8
    add r1, r1, r5
    str r0, [r1, #0x8]
    ldr r0, =native_data13_0221c15c
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    add r0, r0, r5
    ldr r0, [r0, #0x8]
    mov r3, #0x0
    bl native_fn_02202eb0
    ldr r0, =native_data13_0221c15c
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    add r0, r0, r5
    ldr r0, [r0, #0x8]
    mov r2, #0x0
    bl native_fn_02202f54
    ldr r0, =native_data2_0220bb3c
    add r4, r4, #0x1
    ldrb r0, [r0, r7]
    add r6, r6, #0x1
    add r5, r5, #0x4
    cmp r4, r0
    blt ov006_02200344_La2
ov006_02200344_Lea:
    add r0, sp, #0x18
    str r0, [sp]
    mov r0, #0x0
    mov r1, #0x20
    mov r2, #0xc
    mov r3, #0x1
    str r0, [sp, #0x4]
    bl native_fn_0220342c
    ldr r1, =native_data13_0221c15c
    ldr r1, [r1, #0]
    str r0, [r1, #0x10]
    mov r0, #0x0
    ldr r1, [sp, #0x18]
    add r2, r0, #0x0
    bl native_fn_02202c5c
    ldr r1, =native_data13_0221c15c
    lsl r4, r7, #0x2
    ldr r1, [r1, #0]
    str r0, [r1, #0x4]
    bl native_fn_021f290c
    ldr r1, =native_data_0220bac6
    ldr r3, =native_data_0220bac4
    ldrh r1, [r1, r4]
    ldrh r3, [r3, r4]
    str r1, [sp]
    mov r1, #0x2
    str r1, [sp, #0x4]
    str r0, [sp, #0x8]
    ldr r0, [sp, #0x14]
    mov r1, #0x0
    str r0, [sp, #0xc]
    ldr r0, =native_data13_0221c15c
    add r2, r1, #0x0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x10]
    bl native_fn_022037c0
    ldr r0, =native_data13_0221c15c
    mov r1, #0x1
    ldr r3, [r0, #0]
    mov r2, #0x0
    str r2, [sp]
    ldr r0, [r3, #0x10]
    ldr r3, [r3, #0x4]
    lsl r1, r1, #0x8
    bl native_fn_02203848
    mov r0, #0x0
    add r1, r0, #0x0
    mov r2, #0x1f
    add r3, r0, #0x0
    bl native_fn_02203a80
    ldr r3, =native_data13_0221c15c
    mov r0, #0x0
    ldr r3, [r3, #0]
    mov r1, #0x1
    ldrb r4, [r3, #0x1c]
    add r3, sp, #0x1c
    mov r2, #0x1f
    ldrb r3, [r3, r4]
    bl native_fn_02203a80
    mov r0, #0x0
    mov r1, #0x3
    mov r2, #0x1f
    mov r3, #0x1
    bl native_fn_02203a80
    ldr r2, =native_data_0220ba8a
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_022039a4
    mov r0, #0xc0
    bl native_fn_02200770
    mov r2, #0x1
    lsl r2, r2, #0x1a
    ldr r1, [r2, #0]
    ldr r0, =0xffff1fff
    and r1, r0
    mov r0, #0x6
    lsl r0, r0, #0xc
    orr r0, r1
    str r0, [r2, #0]
    ldr r0, [sp, #0x10]
    cmp r0, #0x0
    beq ov006_02200344_L1b8
    ldr r1, =native_fn_02200598+1
    mov r0, #0x1
    mov r2, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data13_0221c15c
    add sp, #0x24
    ldr r1, [r1, #0]
    str r0, [r1, #0x14]
    pop {r4, r5, r6, r7, pc}
ov006_02200344_L1b8:
    ldr r1, =native_fn_022005d8+1
    mov r0, #0x1
    mov r2, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data13_0221c15c
    ldr r1, [r1, #0]
    str r0, [r1, #0x14]
    add sp, #0x24
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
