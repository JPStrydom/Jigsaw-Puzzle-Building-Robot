#ifndef MACROS_H
#define MACROS_H



#define LED_ON				PORTD |= (1<<PORTD6)
#define LED_OFF				PORTD &= ~(1<<PORTD6)
#define LED_TOGGLE			PIND |= (1<<PORTD6)


#define MOTOR_X_RIGHT		PORTB |= (1<<PORTB0)
#define MOTOR_X_LEFT		PORTB &= ~(1<<PORTB0)

#define MOTOR_X_STEP_ON		PORTB |= (1<<PORTB1)
#define MOTOR_X_STEP_OFF	PORTB &= ~(1<<PORTB1)

#define MOTOR_X_WAKE		PORTB |= (1<<PORTB2)
#define MOTOR_X_SLEEP		PORTB &= ~(1<<PORTB2)

#define MOTOR_Y_DOWN		PORTB |= (1<<PORTB3)
#define MOTOR_Y_UP			PORTB &= ~(1<<PORTB3)

#define MOTOR_Y_STEP_ON		PORTB |= (1<<PORTB4)
#define MOTOR_Y_STEP_OFF	PORTB &= ~(1<<PORTB4)

#define MOTOR_Y_WAKE		PORTB |= (1<<PORTB5)
#define MOTOR_Y_SLEEP		PORTB &= ~(1<<PORTB5)

#define MOTOR_R_STEP_ON		PORTB |= (1<<PORTB6)
#define MOTOR_R_STEP_OFF	PORTB &= ~(1<<PORTB6)

#define MOTOR_R_WAKE		PORTB |= (1<<PORTB7)
#define MOTOR_R_SLEEP		PORTB &= ~(1<<PORTB7)


#define ACTUATOR_RESET		OCR1A = 140					//143 //160
#define ACTUATOR_RAISE		OCR1A = 140; _delay_ms(250)	//143 //160
#define ACTUATOR_LOWER_1	OCR1A = 375; _delay_ms(250)	//373 //390
#define ACTUATOR_LOWER_2	OCR1A = 345; _delay_ms(250)	//343 //360
#define ACTUATOR_LOWER_3	OCR1A = 315; _delay_ms(250) //313 //330
#define ACTUATOR_LOWER_4	OCR1A = 300; _delay_ms(250) //298 //315
#define ACTUATOR_LOWER_R_1	OCR1A = 270; _delay_ms(250) //270 //285
#define ACTUATOR_LOWER_R_2	OCR1A = 225; _delay_ms(250) //230 //245
#define ACTUATOR_LOWER_P	OCR1A = 365; _delay_ms(250)	//363 //380
#define ACTUATOR_DELAY		

#define VACUUM_RESET		OCR1B = 300
#define VACUUM_SUCK			OCR1B = 550; _delay_ms(750)
#define VACUUM_BLOW			OCR1B = 250; _delay_ms(750)


#define INT_X_0				(PINA & (1<<PINA0))
#define INT_X_1				(PINA & (1<<PINA1))
#define INT_Y_0				(PINA & (1<<PINA2))
#define INT_Y_1				(PINA & (1<<PINA3))
#define BUTTON				(PIND & (1<<PIND7))


#define STEP_PERIOD_F		500  // us
#define STEP_PERIOD_M		1500 // us
#define STEP_PERIOD_S		5000 // us

#define STEP_PERIOD_R		2000 // us

#define SEPARATION_STEP		200



#endif