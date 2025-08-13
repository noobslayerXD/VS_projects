LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY wrong_code IS
	PORT (
		clk : IN STD_LOGIC;
		reset : IN STD_LOGIC;
		err_event : IN STD_LOGIC;
		failed : OUT STD_LOGIC
	);
END wrong_code;

ARCHITECTURE wrong OF wrong_code IS
	TYPE state IS (idle, err_0, err_1, err_2, Unlocked, wrong_code, perm_lock);
	SIGNAL present_state, next_state : state;
BEGIN
	PROCESS (clk, reset,next_state)
	BEGIN
		IF reset = '1' THEN
			errors <= "00"; -- Reset errors to zero on reset signal
		ELSIF rising_edge(clk) THEN
			when err_0 =>
				if error_event='1'; then
				next_state <= err_1;
				else 
					next_state <= err_0;
			
		END IF;
	END PROCESS;
END wrong;