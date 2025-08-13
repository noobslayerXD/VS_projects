LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY three_process_fsm_template IS
	PORT (
		-- Inputs
		reset : IN STD_LOGIC;
		b : IN STD_LOGIC;
		a : IN STD_LOGIC;
		clk : IN STD_LOGIC;
		-- Outputs
		meeout : OUT STD_LOGIC;
		mooout : OUT STD_LOGIC
	);
END three_process_fsm_template;

ARCHITECTURE three_processes OF three_process_fsm_template IS
	-- Define the states of the FSM
	TYPE state IS (idle, init, aktiv);
	SIGNAL present_state, next_state : state;
BEGIN
	-- Process for state registration
	state_reg : PROCESS (clk)
	BEGIN
		IF rising_edge(clk) THEN
			-- State registration with reset handling
			IF reset = '0' THEN
				present_state <= idle;
			ELSE
				present_state <= next_state;
			END IF;
		END IF;
	END PROCESS;

	-- Process for determining the next state based on current inputs and state
	nxt_state : PROCESS (present_state, clk, reset, a, b)
	BEGIN
		CASE present_state IS
			WHEN idle =>
				-- Define conditions for transitioning to the next state
				IF b = '1' THEN
					next_state <= init;
				ELSE
					next_state <= present_state;
				END IF;
			WHEN init =>
				IF b = '1' AND a = '0' THEN
					next_state <= present_state;
				ELSIF b = '0' AND a = '1' THEN
					next_state <= aktiv;
				ELSE
					next_state <= idle;
				END IF;
			WHEN aktiv =>
				-- Set the next state based on the current state
				next_state <= idle;
				-- Default branch
			WHEN OTHERS =>
				present_state <= next_state;
		END CASE;
	END PROCESS;

	-- Process for generating outputs based on the current state
	outputs : PROCESS (present_state, clk, reset, a, b)
	BEGIN
		CASE present_state IS
				-- Define outputs for each state
			WHEN idle =>
				mooout <= '0';
				meeout <= '0';
			WHEN init =>
				-- Set outputs based on conditions
				mooout <= '1';
				IF b = '1' AND a = '1' THEN
					meeout <= '1';
				ELSE
					meeout <= '0';
				END IF;
			WHEN aktiv =>
				meeout <= '0';
				mooout <= '1';
				-- Default branch
			WHEN OTHERS =>
				meeout <= '0';
				mooout <= '0';
		END CASE;
	END PROCESS;
END three_processes;