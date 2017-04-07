/*
 * Puzzle_Solver.c
 *
 * Created: 2016/08/20 5:35:55 PM
 * Author : JP
 */ 

#define F_CPU 16000000UL		// 16 MHz clock
#define FOSC F_CPU				// Clock speed for BAUD rate 
#define BAUD 38400				// 38.4 KHz BAUD rate
#define MYUBRR FOSC/16/BAUD-1	// Set BAUD rate calculation parameter

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <string.h>

#include "macros.h"


// Functions Definitions
// =====================================
void IO_Init(void);
void Interrupt_Init(void);
void PWM_Init(void);
void USART_Init(int);

void USART_Transmit_Byte(char);
char USART_Receive_Byte(void);
void USART_Transmit(char*);
void USART_Receive(void);

int* Get_Coordinates(char*);
int Str_To_Int(char*);

void Move(int*);
void Rotate(int*);
void Separate(int*);
void Place(int*);
void Reset(void);
void Update(int, int);

int* adjust_coordinates(int*);
void set_gantry(int, int, int);
void pick_up(int);
void put_down(int);
void rotate_help(int);
void pick_up_separate();
// =====================================


// Global Variables
// =====================================
volatile int x_step_count = 0;
volatile int y_step_count = 0;

volatile char message[100];

volatile int Port_A_History = 0;
// =====================================

int main(void)
{	
	IO_Init();			// Setup IO pins
	Interrupt_Init();	// Setup interrupts
	PWM_Init();			// Setup PWM
	USART_Init(MYUBRR); // Setup USART
	
	sei();				// Enable global interrupts
	
	_delay_ms(1000);
	
	Reset();

	while(1)
	{
		USART_Receive();	
		
		if(strstr(message, "M") != NULL)
		{
			int* coordinate = Get_Coordinates(message);
			LED_ON;
			Move(coordinate);
			LED_OFF;
		}
		else if(strstr(message, "R") != NULL)
		{
			int* coordinate = Get_Coordinates(message);
			LED_ON;
			Rotate(coordinate);
			LED_OFF;
		}
		else if(strstr(message, "S") != NULL)
		{
			int* coordinate = Get_Coordinates(message);
			LED_ON;
			Separate(coordinate);
			LED_OFF;
		}
		else if(strstr(message, "P") != NULL)
		{
			int* coordinate = Get_Coordinates(message);
			LED_ON;
			Place(coordinate);
			LED_OFF;
		}
		else if(strstr(message, "E") != NULL)
		{
			LED_ON;
			Reset();
			LED_OFF;
		}
		else if(strstr(message, "U") != NULL)
		{
			int* coordinate = Get_Coordinates(message);
			Update(coordinate[0], coordinate[1]);
		}
		else if(strstr(message, "T") != NULL)
		{
			int* coordinate = Get_Coordinates(message);
			ACTUATOR_RAISE;
			set_gantry(coordinate[0], coordinate[1], 1);
			ACTUATOR_LOWER_R_2;
		}
		USART_Transmit("D\r\n");
	}
	
	return 0;
}

ISR(PCINT0_vect)
{
	int Port_A_Change = PINA ^ Port_A_History;
	Port_A_History = PINA;

	if(Port_A_Change & (1<<PINA0))
	{
		if(INT_X_0)
		{
			MOTOR_X_SLEEP;
		}
	}

	if(Port_A_Change & (1<<PINA1))
	{
		if(INT_X_1)
		{
			MOTOR_X_SLEEP;
		}
	}

	if(Port_A_Change & (1<<PINA2))
	{
		if(INT_Y_0)
		{
			MOTOR_Y_SLEEP;
		}
	}
	
	if(Port_A_Change & (1<<PINA3))
	{
		if(INT_Y_1)
		{
			MOTOR_Y_SLEEP;
		}
	}
}

void IO_Init (void)
{
	// 1 = output, 0 = input
	DDRA &= ~(1<<PORTA0) & ~(1<<PORTA1) & ~(1<<PORTA2) & ~(1<<PORTA3);														// Set PA0 - PA3 as inputs (= 0)
	
	DDRB |= (1<<PORTB0) | (1<<PORTB1) | (1<<PORTB2) | (1<<PORTB3) | (1<<PORTB4) | (1<<PORTB5) | (1<<PORTB6) | (1<<PORTB7);	// Set PB0 - PB7 as outputs (= 1)
	
	DDRD &= ~(1<<PORTD0) & ~(1<<PORTD7);																					// Set PD0 & PD7 as inputs (= 0)
	DDRD |= (1<<PORTD1) | (1<<PORTD4) | (1<<PORTD5) | (1<<PORTD6);															// Set PD1, & PD4 - PD6 as outputs (= 1) 
	
	return;
}
void Interrupt_Init()
{
	PCICR |= (1<<PCIE0);												// Enable Pin Change Interrupts 0 to 7
	PCMSK0 |= (1<<PCINT0) | (1<<PCINT1) | (1<<PCINT2) | (1<<PCINT3);	// Enable Pin Change Interrupt 0 - 4 (PA0 - PA3)
	
	return;
}
void PWM_Init()
{
	TCCR1A |= (1<<COM1A1) | (1<<COM1B1) | (1<<WGM11);			// Set up non-inverted PWM on OC1A and OC1B with 16-bit timer
	TCCR1B |= (1<<WGM13) | (1<<WGM12) | (1<<CS11) | (1<<CS10);	// Set fast PWM with ICR1A as TOP and prescaler to 64
	
	ICR1 = 4999;												// Set 50Hz PWM frequency (20ms period)
	
	ACTUATOR_RESET;												// Raise piece actuator
	VACUUM_RESET;											// Release actuator suction
	
	return;
}
void USART_Init(int ubrr)
{
	UBRR0H = (char)(ubrr>>8);			// Set baud rate high byte
	UBRR0L = (char)ubrr;				// Set baud rate low byte	
	
	UCSR0B = (1<<RXEN0) | (1<<TXEN0);	// Enable receiver and transmitter
	
	UCSR0C = (3<<UCSZ00);				// Set frame format: 8 bit data, 1 stop bit
	
	return;
}

void USART_Transmit_Byte(char data)
{
	while ( !( UCSR0A & (1<<UDRE0)) );	// Wait for empty transmit buffer
	
 	UDR0 = data;						// Put data into buffer, sends the data
	 
	 return;
}
char USART_Receive_Byte(void)
{
	while ( !(UCSR0A & (1<<RXC0)) );	// Wait for data to be received
	
	return UDR0;						// Get and return received data from buffer
}
void USART_Transmit(char* string)
{
	for (int i = 0; string[i] != '\0'; i++) // Transmit each character until end-of-string character
	{
		USART_Transmit_Byte(string[i]);
	}
	
	return;
}
void USART_Receive(void)
{
	int i = 0;
	message[i] = USART_Receive_Byte();
	
	for(i = 1; message[i-1] != '\r'; i++)	// Read and append received characters until a return carriage is seen
	{
		message[i] = USART_Receive_Byte();
	}
	
	message[i] = '\n';						// Append newline character
	
	return;
}

int* Get_Coordinates(char* string)
{
	static int coordinates[6];
	char temp_string[4];

	int start_index = 1;

	for(int i = 0; i < 6; i++)
	{
		while(!isdigit(string[start_index]))
		{
			start_index ++;
		}
		int temp_size = 0;
		for(int j = start_index; isdigit(string[j]); j++)
		{
			temp_string[j-start_index] = string[j];
			temp_size ++;
		}
		temp_string[temp_size] = '\0';
		start_index += temp_size + 1;
		
		coordinates[i] = Str_To_Int(temp_string);
	}
	
	return coordinates;
}
int Str_To_Int(char* string)
{
	if(strlen(string) == 0)
	{
		return 0;
	}
	int integer = 0;
	int buffer = 1;
	for(int i = strlen(string) - 1; i >= 0; i--)
	{
		if(!isdigit(string[i]))
		{
			return 0;
		}
		integer += (string[i]-48)*buffer;
		buffer *= 10;
	}
	
	return integer;
}

void Move(int* coordinate)
{
	coordinate = adjust_coordinates(coordinate);
	set_gantry(coordinate[0], coordinate[1], 1);
	pick_up(coordinate[4]);
	set_gantry(coordinate[2], coordinate[3], 1);
	put_down(coordinate[4]);
	
	return;
}
void Rotate(int* coordinate)
{
	int x_temp = coordinate[2];
	int y_temp = coordinate[3];
	int pick_drop = coordinate[4];
	int degree = coordinate[5];
	
	coordinate[2] = 1945;	// Rotator coordinates 1955
	coordinate[3] = 100;
	coordinate[4] = (pick_drop - pick_drop%10) + 4;
	
	Move(coordinate);
	rotate_help(degree);
	
	coordinate[0] = 1945;	// Rotator coordinates
	coordinate[1] = 100;
	coordinate[2] = x_temp;
	coordinate[3] = y_temp;
	coordinate[4] = 40 + pick_drop%10;
	
	Move(coordinate);
	
	return;
}
void Separate(int* coordinate)
{
	coordinate = adjust_coordinates(coordinate);
	set_gantry(coordinate[0], coordinate[1], 1);
	pick_up_separate(coordinate[4]);
	if(coordinate[5] == 0)
	{
		set_gantry(coordinate[0], coordinate[1] - SEPARATION_STEP, 2);
	}
	else if(coordinate[5] == 1)
	{
		set_gantry(coordinate[0] + SEPARATION_STEP, coordinate[1], 2);
	}
	else if(coordinate[5] == 2)
	{
		set_gantry(coordinate[0], coordinate[1] + SEPARATION_STEP, 2);
	}
	else
	{
		set_gantry(coordinate[0] - SEPARATION_STEP, coordinate[1], 2);
	}
	ACTUATOR_RAISE;
	set_gantry(coordinate[2], coordinate[3], 1);
	put_down(coordinate[4]);
	
	return;
}
void Place(int* coordinate)
{
	set_gantry(coordinate[0], coordinate[1], 1);
	ACTUATOR_LOWER_P;
	set_gantry(coordinate[2], coordinate[3], 2);
	ACTUATOR_RAISE;
	
	return;
}
void Reset()
{
	ACTUATOR_RESET;
	if(INT_X_0)
	{
		MOTOR_X_SLEEP;
	}
	else
	{
		MOTOR_X_LEFT;
		MOTOR_X_WAKE;
	}
	
	if(INT_Y_0)
	{
		MOTOR_Y_SLEEP;
	}
	else
	{
		MOTOR_Y_UP;
		MOTOR_Y_WAKE;
	}
	
	while(!INT_X_0 || !INT_Y_0)
	{
		MOTOR_X_STEP_ON;
		MOTOR_Y_STEP_ON;
		_delay_us(STEP_PERIOD_F);
		MOTOR_X_STEP_OFF;
		MOTOR_Y_STEP_OFF;
		_delay_us(STEP_PERIOD_F);
	}
	_delay_ms(100);
	
	MOTOR_X_RIGHT;
	MOTOR_Y_DOWN;
	
	MOTOR_X_WAKE;
	MOTOR_Y_WAKE;
	
	int x_search = 1;
	int y_search = 1;
	
	while(INT_X_0 || INT_Y_0)
	{
		if(x_search)
		{
			MOTOR_X_STEP_ON;
		}
		if(y_search)
		{
			MOTOR_Y_STEP_ON;
		}
		_delay_us(STEP_PERIOD_M);
		MOTOR_X_STEP_OFF;
		MOTOR_Y_STEP_OFF;
		_delay_us(STEP_PERIOD_M);
		
		if(!INT_X_0)
		{
			x_search = 0;
		}
		else if(x_search)
		{
			MOTOR_X_WAKE;
		}
		
		if(!INT_Y_0)
		{
			y_search = 0;
		}
		else if(y_search)
		{
			MOTOR_Y_WAKE;
		}
	}
	_delay_ms(100);
	MOTOR_X_SLEEP;
	MOTOR_Y_SLEEP;
	
	x_step_count = 0; // 40
	y_step_count = 0; // 55
	
	return;
}
void Update(int x, int y)
{
	if(x >= 0 && x < 2100)
	{
		x_step_count = x;
	} 
	if(y >= 0 && y < 1650)
	{
		y_step_count = y;
	}
}

int* adjust_coordinates(int* coordinate)
{
	int temp = coordinate[4];
	
	if(temp > 20)
	{
		if(temp < 30)
		{
			coordinate[1] -= 3; // [TESTED]
		}
		else if(temp < 40)
		{
			coordinate[1] -= 21; // [TESTED]
		}
	}
	
	temp = temp % 10;
	if(temp == 1)
	{
		coordinate[3] -= 2; // [TESTESD]
	}
	else if(temp == 2)
	{
		coordinate[3] -= 4; // [TESTED]
	}
	else if(temp == 3)
	{
		coordinate[3] -= 22; // [TESTED]
	}
	
	return coordinate;
}
void set_gantry(int x_destination, int y_destination, int speed)
{
	if(x_destination > 2100 || y_destination > 1650) 
	{
		return;
	}
	
	int x_location = x_step_count;
	int y_location = y_step_count;
	
	int x_direction;
	int y_direction;
	
	if(x_destination >= x_location)
	{
		MOTOR_X_RIGHT;
		x_direction = 1;
	}
	else
	{
		MOTOR_X_LEFT;
		x_direction = -1;
		////////////////
		// x_location -= 1;
		////////////////
	}

	if(y_destination >= y_location)
	{
		MOTOR_Y_DOWN;
		y_direction = 1;
	}
	else
	{
		MOTOR_Y_UP;
		y_direction = -1;
		////////////////
		// y_location -= 1;
		////////////////
	}
	
	MOTOR_X_WAKE;
	MOTOR_Y_WAKE;
	
	int x_search = 1;
	int y_search = 1;
	
	while(x_search || y_search)
	{
		if(x_location == x_destination && x_search)
		{
			x_step_count = x_location;
			x_search = 0;
		}
		if(y_location == y_destination && y_search)
		{
			y_step_count = y_location;
			y_search = 0;
		}
		
		if(x_search)
		{
			MOTOR_X_STEP_ON;
		}
		if(y_search)
		{
			MOTOR_Y_STEP_ON;
		}
		x_location += x_direction;
		y_location += y_direction;
		if(speed == 1)
		{
			_delay_us(STEP_PERIOD_F);
		}
		else
		{
			_delay_us(STEP_PERIOD_M);
		}
		MOTOR_X_STEP_OFF;
		MOTOR_Y_STEP_OFF;
		if(speed == 1)
		{
			_delay_us(STEP_PERIOD_F);
		}
		else
		{
			_delay_us(STEP_PERIOD_M);
		}
		
	}
	_delay_ms(100);
	MOTOR_X_SLEEP;
	MOTOR_Y_SLEEP;
	
	return;
}
void pick_up(int pick)
{
	if(pick < 20)
	{
		ACTUATOR_LOWER_1;
	}
	else if(pick < 30)
	{
		ACTUATOR_LOWER_2;
	}
	else if(pick < 40)
	{
		ACTUATOR_LOWER_3;
	}
	else if(pick < 50)
	{
		ACTUATOR_LOWER_R_1;
	}
	VACUUM_SUCK;
	ACTUATOR_RAISE;
	
	return;
}
void put_down(int put)
{
	put = put%10;
	if(put == 0)
	{
		ACTUATOR_LOWER_P;
	}
	else if(put == 1)
	{
		ACTUATOR_LOWER_2;
	}
	else if(put == 2)
	{
		ACTUATOR_LOWER_3;
	}
	else if(put == 3)
	{
		ACTUATOR_LOWER_4;
	}
	else if(put == 4)
	{
		ACTUATOR_LOWER_R_2;
	}
	VACUUM_BLOW;
	ACTUATOR_RAISE;
	VACUUM_RESET;
	
	return;
}
void rotate_help(int degree)
{
	degree = degree/0.72 + 1;
	
	MOTOR_R_WAKE;
	
	for(int i = 0; i < degree; i++)
	{
		MOTOR_R_STEP_ON;
		_delay_us(STEP_PERIOD_R);
		MOTOR_R_STEP_OFF;
		_delay_us(STEP_PERIOD_R);
	}
	_delay_ms(100);
	MOTOR_R_SLEEP;
	
	return;
}
void pick_up_separate()
{
	ACTUATOR_LOWER_1;
	VACUUM_SUCK;
	ACTUATOR_LOWER_2;
	
	return;
}