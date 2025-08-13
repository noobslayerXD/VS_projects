LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY Wrong IS
	PORT (
		-- Inputs
		reset : IN STD_LOGIC;
		clk : IN STD_LOGIC;
		err_event : IN STD_LOGIC;
		-- Outputs
		err_count : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
		failed : OUT STD_LOGIC
	);
END Wrong;

ARCHITECTURE processes OF Wrong IS
	-- Define the states of the FSM
	TYPE state IS (idle, err_state0, err_state1, err_state2);
	SIGNAL present_state, next_state : state;
BEGIN
	-- Process for state registration
	state_reg : PROCESS (clk)
	BEGIN
		IF rising_edge(clk) THEN
			IF reset = '0' THEN
				present_state <= idle;
			ELSE
				present_state <= next_state;
			END IF;
		END IF;
	END PROCESS;
	nxt_state : PROCESS (present_state, err_event)
	BEGIN
		CASE present_state IS
				-- one case branch required for each state
			WHEN idle =>
				IF err_event = '1' THEN
					next_state <= err_state0;
				ELSE
					next_state <= idle;
				END IF;
			WHEN err_state0 =>
				IF err_event = '1' THEN
					next_state <= err_state1;
				ELSE
					next_state <= err_state0;
				END IF;
			WHEN err_state1 =>
				IF err_event = '1' THEN
					next_state <= err_state2;
				ELSE
					next_state <= err_state1;
				END IF;
			WHEN err_state2 =>
				next_state <= err_state2;
		END CASE;
	END PROCESS;
	outputs : PROCESS (present_state, err_event)
	BEGIN
		CASE present_state IS
			WHEN err_state2 =>
				failed <= '1';
				err_count <= "11";
			WHEN err_state1 =>
				err_count <= "10";
				failed <= '0';
			WHEN err_state0 =>
				err_count <= "01";
				failed <= '0';
			WHEN OTHERS =>
				failed <= '0';
				err_count <= "00";
		END CASE;
	END PROCESS;
END processes;