LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY code_lock_simple_fsm IS

	PORT (
		--In	
		reset : IN STD_LOGIC;
		enter : IN STD_LOGIC;
		code : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		clk : IN STD_LOGIC;
		failed : IN STD_LOGIC;
		--Out
		lock : OUT STD_LOGIC;
		lock0 : OUT STD_LOGIC;
		err_event : OUT STD_LOGIC
	);
END code_lock_simple_fsm;

ARCHITECTURE processes OF code_lock_simple_fsm IS
	TYPE state IS (idle, Ev_code1, get_code2, Ev_code2, Unlocked, perm_lock, wrong_code);
	SIGNAL present_state, next_state : state;

	------ Hardwirede koder til kodelåsen
	SIGNAL code1 : STD_LOGIC_VECTOR(3 DOWNTO 0) := "1100";
	SIGNAL code2 : STD_LOGIC_VECTOR(3 DOWNTO 0) := "1110";
BEGIN
	---STATE Registration----------------------
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
	--------------------------------------------------------

	--- next state---------------------------------------------------
	nxt_state : PROCESS (present_state, code, code1, code2, enter)
	BEGIN
		CASE present_state IS
				-- one case branch required for each state
			WHEN idle =>
				IF failed = '1' THEN
					next_state <= perm_lock;
				ELSE
					next_state <= idle;
				END IF;
				IF enter = '1' THEN
					next_state <= Ev_code1;
				ELSE
					next_state <= idle;
				END IF;
			WHEN Ev_code1 =>
				IF code = code1 THEN
					next_state <= get_code2;
				ELSE
					next_state <= idle;
					-- Set err_event to '1' when code1 is not equal to code
					IF code1 /= code THEN
						next_state <= wrong_code;
					ELSE
						next_state <= ev_code1;
					END IF;
				END IF;
			WHEN get_code2 =>
				IF enter = '1' THEN
					next_state <= Ev_code2;
				ELSE
					next_state <= get_code2;
				END IF;
			WHEN Ev_code2 =>
				IF code = code2 THEN
					next_state <= Unlocked;
				ELSE
					next_state <= idle;
					-- Set err_event to '1' when code2 is not equal to code
					IF code2 /= code THEN
						next_state <= wrong_code;
					ELSE
						next_state <= idle;
					END IF;
				END IF;
			WHEN Unlocked =>
				IF enter = '1' THEN
					next_state <= idle;
				ELSE
					next_state <= Unlocked;
				END IF;
			WHEN wrong_code =>
				IF failed = '1' THEN
					next_state <= perm_lock;
				ELSE
					next_state <= idle;
				END IF;
			WHEN perm_lock =>
				next_state <= perm_lock;
				-- default branch
			WHEN OTHERS =>
				next_state <= idle;
		END CASE;
	END PROCESS;
	----------------------------------------------------------------
	--------- outputs -----------------------------------------------
	outputs : PROCESS (present_state, code, code1, code2, enter)
	BEGIN
		CASE present_state IS
				-- one case branch required for each state
			WHEN Unlocked =>
				IF enter = '1' THEN
					lock <= '1';
					lock0 <= '0';
				ELSE
					lock <= '0';
					lock0 <= '1';
					err_event <= '0';
				END IF;
			WHEN wrong_code =>
				err_event <= '1';
				lock <= '1';
				lock0 <= '0';
				-- default branch
			WHEN OTHERS =>
				lock <= '1';
				lock0 <= '0';
				err_event <= '0';
		END CASE;
	END PROCESS;
	-------------------------------------------------------------------
END processes;