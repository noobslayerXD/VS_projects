/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/

#include "project.h"

CY_ISR_PROTO(ISR_UART_rx_handler);
void handleByteReceived(uint8_t byteReceived);
void decreaseSpeed(void);
void increaseSpeed(void);
void driveForwards(void);
void driveBackwards(void);
void stop(void);

uint8_t speed = 125;

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    isr_uart_rx_StartEx(ISR_UART_rx_handler);
    UART_1_Start();
    PWM_1_Start();
    
    UART_1_PutString("DC-Motor-PWM application started\r\n");
    UART_1_PutString("0: Stop\r\n");
    UART_1_PutString("1: Drive forwards\r\n");
    UART_1_PutString("2: Drive backward\r\n");
    UART_1_PutString("q: Decrease speed\r\n");
    UART_1_PutString("w: Increase speed\r\n");

    for(;;)
    {
        /* Place your application code here. */
    }
}

CY_ISR(ISR_UART_rx_handler)
{
    uint8_t bytesToRead = UART_1_GetRxBufferSize();
    while (bytesToRead > 0)
    {
        uint8_t byteReceived = UART_1_ReadRxData();
        UART_1_WriteTxData(byteReceived); // echo back
        
        handleByteReceived(byteReceived);
        
        bytesToRead--;
    }
}

void handleByteReceived(uint8_t byteReceived)
{
    switch(byteReceived)
    {
        case 'q':
            decreaseSpeed();
            break;
        case 'w':
            increaseSpeed();
            break;
        case '1':
            driveForwards();
            break;
        case '2':
            driveBackwards();
            break;
        case '0':
            stop();
            break;
        default:
            // nothing
            break;
    }
}

void decreaseSpeed()
{
    if (speed > 0)
    {
        UART_1_PutString("Decreasing speed\r\n");
        speed -= 5;
        PWM_1_WriteCompare(speed);
        
    }
    else 
    {
        UART_1_PutString("TOO SLOW\r\n");
    }
}

void increaseSpeed()
{
    if (speed < 255)
    {
        UART_1_PutString("Increasing speed\r\n");
        speed += 5;
        PWM_1_WriteCompare(speed);
        
    }
    else 
    {
        UART_1_PutString("TOO FAST\r\n");
    }
}

void driveForwards()
{
    UART_1_PutString("Set direction: forwards\r\n");
    V_en_Write(1);
    D_Write(0);
    C_Write(1);
}

void driveBackwards()
{
    UART_1_PutString("Set direction: backward\r\n");
    V_en_Write(1);
    D_Write(1);
    C_Write(0   );
}

void stop()
{
    UART_1_PutString("Stop\r\n");
    PWM_1_WriteCompare(0); // Stop the motor
}

/* [] END OF FILE */
