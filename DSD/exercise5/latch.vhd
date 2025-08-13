LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY mylatch IS

	PORT (
		-- Input ports
		set : IN STD_LOGIC;
		input : IN STD_LOGIC_VECTOR(7 DOWNTO 0);

		-- Output ports
		set_val : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
	);
END mylatch;
ARCHITECTURE latch_impl OF mylatch IS
BEGIN
	PROCESS (input, set)
	BEGIN
		IF set = '1' THEN
			-- When set is asserted, the latch stores the input values
			set_val <= input;
		END IF;
	END PROCESS;
END latch_impl;